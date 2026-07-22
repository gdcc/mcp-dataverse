import asyncio
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

async def main():
    async with sse_client("http://localhost:8000/sse") as streams:
        async with ClientSession(streams[0], streams[1]) as session:
            await session.initialize()
            print("Initialized")
            tools = await session.list_tools()
            print(tools)

asyncio.run(main())
