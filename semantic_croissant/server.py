from datetime import datetime
import json
import logging
import sys
from typing import Optional
import urllib
import os
import time
from urllib.error import HTTPError
import asyncio
import anyio
import click
from fastapi import Body
from fastapi import Request
from fastapi import Response
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import httpx
from mcp.server.lowlevel import Server
from mcp.server.fastmcp import FastMCP
from mcp.server.session import ServerSession
import mcp.types as types
from pyDataverse.Croissant import Croissant
import requests
#from mcp.server.lowlevel import TextContent
#from mcp.schema import TextContent
#from utils.MultiMedia import MultiMedia
import pydoi

from utils.dataframe import CroissantRecipe
####################################################################################
# Temporary monkeypatch which avoids crashing when a POST message is received
# before a connection has been initialized, e.g: after a deployment.
# pylint: disable-next=protected-access
old__received_request = ServerSession._received_request


async def _received_request(self, *args, **kwargs):
    try:
        return await old__received_request(self, *args, **kwargs)
    except RuntimeError:
        pass


# pylint: disable-next=protected-access
ServerSession._received_request = _received_request
####################################################################################\
logger = logging.getLogger(__name__)

def resolve_doi( doi_str):
    if not doi_str.startswith('doi:'):
        doi_str = f"doi:{doi_str}"
    doi = pydoi.get_url(urllib.parse.quote(doi_str.replace("doi:", "")))
    print(doi)
    if 'http' in doi:
        return f"{urllib.parse.urlparse(doi).scheme}://{urllib.parse.urlparse(doi).hostname}"
    else:
        print(f"DOI is {doi}")
        return None

async def fetch_website(
    url: str,
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    headers = {
        "User-Agent": "MCP Croissant Server"
    }
    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:
        response = await client.get(url)
        response.raise_for_status()
        #return [types.TextContent(type="text", text=response.text)]
        return response.text

def serialize_data(data):
    """Recursively convert datetime objects to strings."""
    if isinstance(data, dict):
        return {k: serialize_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [serialize_data(item) for item in data]
    elif isinstance(data, datetime):  # Ensure you import datetime
        return data.isoformat()  # Convert datetime to ISO format string
    return data

def convert_dataset_to_croissant_ml(doi: str, max_retries: int = 3, retry_delay: int = 5) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    if not doi.startswith('doi:'):
        doi = f"doi:{doi}"
    host = resolve_doi(doi)

    print(f"Getting Croissant record for Dataverse doi: {doi}", file=sys.stderr)
    
    for attempt in range(max_retries):
        try:
            croissant = Croissant(doi=doi, host=host)
            record = croissant.get_record()
            return record
        except HTTPError as e:
            if e.code == 429 and attempt < max_retries - 1:
                print(f"Rate limited, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})", file=sys.stderr)
                time.sleep(retry_delay)
                continue
            raise
        except Exception as e:
            logger.error(f"Error fetching record: {e}")
            return {"error": "Unable to fetch record from Dataverse."}
    
    return {"error": "Maximum retry attempts reached. Please try again later."}

def datatool(input: dict) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    doi = input["doi"]
    file = input["file"]
    logger.info(f"Datatool DOI is {doi}")
    semantic_croissant = CroissantRecipe(doi)
    semantic_croissant.get_files()

    # Process all files
    semantic_croissant.process_all_files(file)
    serializable_columns = {k: {col: str(v) for col, v in v.items()} for k, v in semantic_croissant.columns.items()}
    logger.info(serializable_columns)
    return serializable_columns


@click.command()
@click.option("--port", default=8000, help="Port to listen on for SSE")
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def main(port: int, transport: str) -> int:
    app = Server("semantic-croissant")

    @app.call_tool()
    async def fetch_tool(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name != "fetch":
            raise ValueError(f"Unknown tool: {name}")
        if "url" not in arguments:
            raise ValueError("Missing required argument 'url'")
        return await fetch_website(arguments["url"])

    @app.call_tool()
    async def get_croissant_record(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        logger.info(f"Tool name received: {name}")
        if name != "get_croissant_record":
            raise ValueError(f"Unknown tool: {name}")
        return convert_dataset_to_croissant_ml(arguments["doi"])

    @app.call_tool()
    async def datatool(
        name: str, input: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name != "datatool":
            raise ValueError(f"Unknown tool: {name}")
        return await datatool(input)

    @app.call_tool()
    async def get_croissant_record_endpoint(
        name: str, arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name != "get_croissant_record":
            raise ValueError(f"Unknown tool: {name}")
        #await asyncio.sleep(0.1)
        record = convert_dataset_to_croissant_ml(arguments["doi"]) #await get_croissant_record("get_croissant_record", {"doi": arguments["doi"]})
        return record
        #serializable_record = serialize_data(record)
        #return types.TextContent(type="text", text=json.dumps(serializable_record, indent=4))

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        tools = [
            types.Tool(
                name="fetch",
                endpoint="/fetch",
                description="Fetches a website and returns its content",
                inputSchema={
                    "type": "object",
                    "required": ["url"],
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to fetch",
                        }
                    },
                },
            ),
            types.Tool(
                name="get_croissant_record",
                endpoint="/get_croissant_record",
                description="Convert a dataset to Croissant ML format with get_croissant_record tool and explore the dataset with DOI or handle.",
                inputSchema={
                    "type": "object",
                    "required": ["doi"],
                    "properties": {
                        "doi": {"type": "string", "description": "DOI of the dataset"}
                    },
                },
            ),
            types.Tool(
                name="datatool",
                endpoint="/tools/datatool",
                description="Process a file in a dataset with DOI with datatool tool",
                inputSchema={
                    "type": "object",
                    "required": ["doi", "file"],
                    "properties": {
                        "doi": {"type": "string", "description": "DOI of the dataset"},
                        "file": {"type": "string", "description": "File to process"}
                    },
                },
            ),
            types.Tool(
                name="overview",
                endpoint="/overview",
                description="Get an overview of the Dataverse installations around the world sorted by country. Entrance point for the overview tools if no hosts are provided.",
                inputSchema={
                    "type": "object",
                    "required": [],
                    "properties": {},
                },
            ),
            types.Tool(
                name="overview_datasets",
                endpoint="/overview/datasets",
                description="Get an overview of the Dataverse datasets statistics by host",
                inputSchema={
                    "type": "object",
                    "required": ["host"],
                    "properties": {
                        "host": {"type": "string", "description": "Host of the Dataverse installation (e.g. dataverse.nl)"}
                    },
                },
            ),
            types.Tool(
                name="overview_files",
                endpoint="/overview/files",
                description="Get an overview of the Dataverse files statistics by host",
                inputSchema={
                    "type": "object",
                    "required": ["host"],
                    "properties": {
                        "host": {"type": "string", "description": "Host of the Dataverse installation (e.g. dataverse.nl)"}
                    },
                },
            ),
            types.Tool(
                name="search_datasets",
                endpoint="/search/datasets",
                description="Search for datasets in a Dataverse installation",
                inputSchema={
                    "type": "object",
                    "required": ["host", "query"],
                    "properties": {
                        "host": {"type": "string", "description": "Host of the Dataverse installation (e.g. dataverse.nl)"},
                        "query": {"type": "string", "description": "Query to search for datasets"}
                    },
                },
            ),
        ]
        return tools

    if transport == "sse":
        from fastapi.responses import JSONResponse
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Mount
        from starlette.routing import Route

        sse = SseServerTransport("/messages/")

        async def handle_sse(request):
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )

        async def get_tools(request: Request):
            tools = await list_tools()
            # Convert tools to a serializable format
            serializable_tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema,
                    "endpoint": tool.endpoint
                }
                for tool in tools
            ]
            return JSONResponse(content={"tools": serializable_tools})

        async def get_status(request: Request):
            return JSONResponse(content={"status": "ok"})

        async def run_get_croissant_record(request: Request):
            if request.method == "GET":
                doi = request.query_params.get("doi")
            else:
                body = await request.json()
                doi = body.get("doi")
                host = None

            if not doi:
                return JSONResponse(content={"error": "Missing required field 'doi'. Please provide a DOI in the format '10.18710/CHMWOB'"}, status_code=200)
            
            try:
                result = convert_dataset_to_croissant_ml(doi)
                serialized_result = serialize_data(result)
                return JSONResponse(content=serialized_result)
            except Exception as e:
                logger.error(f"Error in get_croissant_record: {e}")
                return JSONResponse(content={"error": str(e)}, status_code=500)

        async def run_datatool(request: Request):
            if request.method == "GET":
                doi = request.query_params.get("doi")
                file = request.query_params.get("file")
            else:
                body = await request.json()
                doi = body.get("doi")
                file = body.get("file")

            if not doi or not file:
                return JSONResponse(content={"error": "Missing required fields 'doi' and 'file'"}, status_code=400)

            try:
                input_data = {"doi": doi, "file": file}
                result = await datatool(input_data)
                serialized_result = serialize_data(result)
                return JSONResponse(content=serialized_result)
            except Exception as e:
                logger.error(f"Error in datatool: {e}")
                return JSONResponse(content={"error": str(e)}, status_code=500)

        async def get_mcp(request: Request):
            tools = await list_tools()
            # Convert tools to a serializable format
            serializable_tools = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema,
                    "endpoint": tool.endpoint
                }
                for tool in tools
            ]
            return JSONResponse(content={"tools": serializable_tools})

        async def mcp_croissant_record_endpoint(request: Request):
            logger.info(f"New croissant record endpoint called")
            data = await request.json()
            if request.method == "POST":
                doi = data.get("doi")
            else:
                doi = request.query_params.get("doi")
            #return {"status": "ok", "doi": doi}

            if request.method == "GET":
                doi = request.query_params.get("doi")
            else:
                body = await request.json()
                doi = body.get("doi")

            if not doi:
                return JSONResponse(content={"error": "Missing required field 'doi'. Please provide a DOI in the format '10.18710/CHMWOB'"}, status_code=200)

            logger.info(f"New croissant record endpoint called with doi: {doi}")
            try:
                result = await get_croissant_record_endpoint('get_croissant_record', {"doi": doi})
                logger.info(f"Result: {result}")
                serialized_result = serialize_data(result)
                ##return JSONResponse(content=types.TextContent(type="text", text=str(serialized_result)))
                serialized_result['format'] = 'application/json'
                serialized_result['message'] = 'Croissant record fetched successfully'
                #return JSONResponse(content=serialized_result, media_type='application/json')
                #return TextContent(text=json.dumps(serialized_result, indent=4), mime_type='application/json')
                return JSONResponse(content={
                    "type": "text",
                    "mimeType": "application/ld+json",
                    "text": json.dumps(serialized_result, indent=2)
                })
                #return JSONResponse(content={"result": f"{serialized_result}"})
            except Exception as e:
                logger.error(f"Error in get_croissant_record: {e}")
                return JSONResponse(content={"error": str(e)}, status_code=500)

        async def run_fetch_website(request: Request):
            url = request.query_params["url"]
            result = await fetch_website(url)
            #serialized_result = serialize_data(result)  # Serialize the result
            #return JSONResponse(content=serialized_result)
            return Response(content=result, media_type="text/html")

        async def run_get_overview(request: Request):
            url = os.environ.get("DATAVERSES")
            data = requests.get(url)
            installations = data.json()['installations']
            return JSONResponse(content={"installations": installations})
            
        async def run_get_overview_datasets(request: Request):
            if request.method == "GET":
                host = request.query_params.get("host")
            else:
                body = await request.json()
                host = body.get("host")

            return search_datasets(host, False)

        async def run_search_datasets(request: Request):
            if request.method == "GET":
                host = request.query_params.get("host")
                query = request.query_params.get("query")
            else:
                body = await request.json()
                host = body.get("host")
                query = body.get("query")
            return search_datasets(host, query)

        def search_datasets(host: str, query: str):
            if query:
                query = f"q={query}"
            else:
                query = "q=%2A"

            if not 'http' in host:
                host = f"https://{host}"
            url = f"{host}/api/search?{query}&type=dataset"
            data = requests.get(url)
            datasets = data.json()['data']
            return JSONResponse(content={"datasets": datasets})

        async def run_get_overview_files(request: Request):
            if request.method == "GET":
                host = request.query_params.get("host")
            else:
                body = await request.json()
                host = body.get("host")

            if not 'http' in host:
                host = f"https://{host}"
            url = f"{host}/api/search?q=*&type=file&per_page=0"
            data = requests.get(url)
            files = data.json()['data']
            return JSONResponse(content={"files": files})


        starlette_app = Starlette(
            debug=True,
            routes=[
                Route("/sse", endpoint=handle_sse),
                Mount("/messages/", app=sse.handle_post_message),
                Route("/tools", endpoint=get_tools, methods=["GET", "POST"]),
                Route("/status", endpoint=get_status),
                Route("/tools/get_croissant_record", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/tools/croissant/dataverse", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/tools/croissant/kaggle", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/croissant/github", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/croissant/huggingface", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/croissant/openml", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/croissant/zenodo", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/croissant/figshare", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/croissant/dspace", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/croissant", endpoint=run_get_croissant_record, methods=["GET", "POST"]),
                Route("/datatool", endpoint=run_datatool, methods=["GET", "POST"]),
                Route("/mcp", endpoint=get_mcp, methods=["GET", "POST"]),
                Route("/mcp/list_tools", endpoint=get_mcp, methods=["GET", "POST"]),
                Route("/get_croissant_record", endpoint=mcp_croissant_record_endpoint, methods=["GET", "POST"]),
                Route("/fetch", endpoint=run_fetch_website, methods=["GET", "POST"]),
                Route("/overview", endpoint=run_get_overview, methods=["GET", "POST"]),
                Route("/overview/datasets", endpoint=run_get_overview_datasets, methods=["GET", "POST"]),
                Route("/search/datasets", endpoint=run_search_datasets, methods=["GET", "POST"]),
                Route("/overview/files", endpoint=run_get_overview_files, methods=["GET", "POST"]),
            ],
        )

        # Ensure the server is ready before starting
        async def startup():
            logger.info("Server is ready to handle requests")

        starlette_app.add_event_handler("startup", startup)

        import uvicorn

        uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    else:
        from mcp.server.stdio import stdio_server
        logger.info("Starting MCP server in stdio mode")
        async def arun():
            try:
                # Initialize the stdio server
                async with stdio_server() as streams:
                    logger.info("Server is ready to handle requests")
                    
                    # Create initialization options
                    init_options = app.create_initialization_options()
                    
                    # Run the app with proper error handling
                    try:
                        await app.run(streams[0], streams[1], init_options)
                    except Exception as e:
                        logger.error(f"Error running app: {e}")
                        raise
                        
            except Exception as e:
                logger.error(f"Error in stdio server: {e}")
                raise

        anyio.run(arun)

    return 0
