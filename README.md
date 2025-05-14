[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/gdcc-mcp-dataverse-badge.png)](https://mseep.ai/app/gdcc-mcp-dataverse)

# MCP (Model Context Protocol) server for Dataverse

Credits: this work is funded by [SSHOC-NL](https://sshoc.nl) project developing [Semantic Croissant](https://docs.google.com/document/d/1fi9Lb6x5Wm0L9CZftqjSGElV_ifcSW_IT-H8ZlpbrtQ/edit?tab=t.0). First version of [Croissant ML](https://docs.mlcommons.org/croissant/docs/croissant-spec.html) export for Dataverse was implemented by Phil Durbin (Harvard IQSS) and Slava Tykhonov (DANS-KNAW).

If you don't know what Croissant ML is — it's a special language for machines, built on top of Schema.org. With Croissant, we aim to solve multilingual challenges and finally speak the same language across the planet.
Even if it's artificial.

Installation:
```
cp .env-sample .env
docker-compose build
docker-compose up -d
```

Go to http://127.0.0.1:8000/tools to get an overview of available tools. We have also deployed official Dataverse MCP server on https://mcp.dataverse.org

You can register MCP in Cursor, Visual Studio or Windsurf Editor, or other IDE with AI Agents support. For example, create configuration file for Cursor [~/.cursor/mcp.json](https://docs.cursor.com/context/model-context-protocol):
```
{
  "mcpServers": {
    "Croissant": {
      "url": "http://127.0.0.1:8000/sse",
      "headers": {
        "Content-Type": "application/json"
      }
    }
}
}
```

## Test Croissant ML support for Dataverse
```
curl -X POST "http://localhost:8000/tools/dataset_convert_to_croissant_ml" -H "Content-Type: application/json" -d '{"doi":"doi:10.7910/DVN/WGCRY7"}'
```

## Connect MCP to your favourite IDE

Type in the chat of Agent:
```
Connect to MCP server running on http://127.0.0.1:8000 and explore all tools with curl command.

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
## Multilingual support

Let's connect to a dataset in Dutch and ask questions in English. Example dataset is taken from [DANS Archaelogy Data Station](https://archaeology.datastations.nl/dataset.xhtml?persistentId=doi:10.17026/AR/IQZTRX):
```
give me overview of doi:10.17026/dans-xv2-dsx6
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
