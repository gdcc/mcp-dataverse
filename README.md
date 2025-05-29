# MCP (Model Context Protocol) server for Dataverse

Credits: this work is funded by the [SSHOC-NL](https://sshoc.nl) project developing [Semantic Croissant](https://docs.google.com/document/d/1fi9Lb6x5Wm0L9CZftqjSGElV_ifcSW_IT-H8ZlpbrtQ/edit?tab=t.0). The first version of [Croissant](https://docs.mlcommons.org/croissant/docs/croissant-spec.html) export for Dataverse was implemented by Philip Durbin (Harvard IQSS) and Slava Tykhonov (DANS-KNAW).

Croissant is a special language for machines, built on top of Schema.org. With Croissant, we aim to solve multilingual challenges and finally speak the same language across the planet.
Even if it's artificial.

## Getting started with mcp.dataverse.org

When getting started, we recommend the public MCP server for Dataverse at <https://mcp.dataverse.org>. (Below you'll also find instructions on how to run the MCP server locally.) You can visit https://mcp.dataverse.org/tools for an inventory of available tools.

You will need an MCP client with AI agent support such as [Cursor](https://www.cursor.com), [Visual Studio Code](https://code.visualstudio.com), or [Windsurf Editor](https://windsurf.com).

### (Optional) Command line test

Before you get too far into configuring your MCP client, you could try this quick test to get information about a dataset by passing its DOI.

```
curl -X POST "https://mcp.dataverse.org/tools/get_croissant_record" -H "Content-Type: application/json" -d '{"doi":"doi:10.7910/DVN/WGCRY7"}'
```

### Configuring your MCP Client

You'll be using https://mcp.dataverse.org/sse as the URL and SSE (Server-Sent Events) as the type of MCP server.

Click the arrow to expand instructions for your MCP client.

<details><summary>Cursor</summary>

Create a configuration file for Cursor at [~/.cursor/mcp.json](https://docs.cursor.com/context/model-context-protocol):

```
{
  "mcpServers": {
    "Croissant": {
      "url": "https://mcp.dataverse.org/sse",
      "headers": {
        "Content-Type": "application/json"
      }
    }
  }
}
```
</details>

Ensure that "auto" is selected as the agent.

<details><summary>Visual Studio Code</summary>

To register the MCP server in Visual Studio Code ([official docs](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)), open settings and search for "mcp". Click the link "edit in settings.json" under "Model Context Protocol server configurations" and paste the "mcp-dataverse" object below, which is shown in a simplified version of that configuration file.

```
{
...
  "mcp": {
    "servers": {
      "mcp-dataverse": {
        "type": "sse",
        "url": "https://mcp.dataverse.org/sse"
      }
    }
  }
...
}
```

Next, click "view", then "open chat". Choose "Agent" in the dropdown that offers "Ask", "Edit", and "Agent".

Your new MCP server should be configured for use but you can check if it are enabled by clicking the "select tools" icon (just below the chat input area) and scrolling down (here you can also try the "add more tools" button).
</details>

### Chat examples

Here are some suggested examples to use when chatting with the MCP server.

#### Explore a dataset

Type in the chat of Agent:
```
Connect to the MCP server running at https://mcp.dataverse.org and explore all tools using the curl command.

Explore dataset doi:10.7910/DVN/6TFFPG
```
If everything is connected properly you should see this response from the Agent:
```
Based on the dataset information, this is a scientific dataset related to quantum physics research. Here are the key details:
Dataset Title: "Replication Data for: All-Optical Photoluminescence Spectra of Nitrogen-Vacancy Ensembles in Diamond at Low Magnetic Fields"
Description:
This dataset contains experimental data from research on Nitrogen-Vacancy (NV) centers in diamond
It includes data shown in both the main text and supplemental material of the associated scientific paper
The research focuses on photoluminescence spectra at low magnetic fields
```

#### Multilingual support

Let's connect to a dataset in Dutch and ask questions in English. Example dataset is taken from [DANS Archaelogy Data Station](https://archaeology.datastations.nl/dataset.xhtml?persistentId=doi:10.17026/AR/IQZTRX):
```
give me an overview of doi:10.17026/dans-xv2-dsx6
```
The response in English:
```
Here's a comprehensive overview of the dataset with DOI 10.17026/AR/IQZTRX:
Basic Information:
Title: "Plangebied Epemawei te Ysbrechtum" (Planning Area Epemawei in Ysbrechtum)
Description: Archaeological investigation report for the Epemawei area in Ysbrechtum
Creator: B.I. van Hoof (RAAP Archeologisch Adviesbureau BV)
Date Created: April 18, 2025
Version: 6.3 build DANS-DataStation-PATCH-10
Key Findings:
Soil investigation revealed:
Tidal deposits
Eroded peat remnants
Middelzee deposits
No evidence of archaeological sites was found
No further archaeological investigation recommended
Content Structure:
The dataset contains 4 files:
RAAPrap_7313_SFEP_20240821.pdf (2.7 MB)
Main report document
Contains detailed findings and analysis
SFEP_boorgegevens.GeoJson (28.4 KB)
Geological data in GeoJSON format
Contains drilling data
SFEP_rapport_meta.ods (22.9 KB)
Report metadata in spreadsheet format
SFEP_tabellijst.ods (11.7 KB)
Table list in spreadsheet format
Technical Information:
License: Creative Commons Attribution 4.0 (CC BY 4.0)
File Formats:
PDF (application/pdf)
GeoJSON (application/octet-stream)
OpenDocument Spreadsheet (application/vnd.oasis.opendocument.spreadsheet)
All files have MD5 checksums for verification
Context:
Location: Ysbrechtum, Netherlands
Type: Archaeological investigation report
Purpose: Planning area assessment
Conducted by: RAAP Archeological Advisory Bureau
This dataset is valuable for:
Archaeological research
Urban planning
Historical geography
Environmental studies
Cultural heritage management
```

## Local installation

```
cp .env-sample .env
docker-compose build
docker-compose up -d
```

Go to http://127.0.0.1:8000/tools to get an overview of available tools.

### Test Croissant support for Dataverse
```
curl -X POST "http://localhost:8000/tools/get_croissant_record" -H "Content-Type: application/json" -d '{"doi":"doi:10.7910/DVN/WGCRY7"}'
```