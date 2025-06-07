# Dataverse MCP Use Cases

The **Dataverse MCP** (Model Context Protocol) enables automated tools and LLM agents to explore and analyze the global Dataverse data network.

## 🚀 Onboarding: Before You Start

To get started, complete onboarding at:

👉 **https://mcp.dataverse.org**

This prepares your agent or system to interact with the MCP tools programmatically.

---

## 🛠 Available Tools

| Tool | Description |
|------|-------------|
| `fetch` | Fetch a website and return its content. |
| `onboarding` | Get onboarding instructions for an LLM or system to act independently. |
| `get_croissant_record` | Convert a dataset to Croissant ML format using DOI or handle. |
| `datatool` | Process and inspect a file in a dataset by DOI and filename. |
| `overview` | Get an overview of all Dataverse installations worldwide. |
| `overview_datasets` | Get dataset statistics for a specific Dataverse host. |
| `overview_files` | Get file statistics for a specific Dataverse host. |
| `search_datasets` | Search datasets within a specific Dataverse installation. |

> ✅ Example: Use `search_datasets` with  
> `{ "query": "climate change", "host": "dataverse.harvard.edu" }`

---

## ❓ Common Questions

- Do onboarding and give me overview of all Dataverses
- List Dataverses from US
- How many datasets in dataverse.nl?
- How many datasets on `{query}` exist in the whole Dataverse network?
- How many Dataverse installations were created over the last 10 years, by country?
- How many datasets exist in France?
- How many datasets on economics are in `dataverse.nl`?
- Which countries have added the most new Dataverse nodes since 2015?
- What kinds of files are in energy consumption datasets from `dataverse.nl`?
- How many datasets were published in France in 2024?
- Compare number of datasets between Johns Hopkins and Harvard Dataverse.
- I'm studying gender inequality in education. What datasets could help?
- give me overview of dataset doi:10.17026/dans-x8n-hfvr 
- where this coin was found?
- what is the age of the coin?

---

## 🇳🇱 Summary: Dutch Dataverses (June 2025)

- **DataverseNL**: 8,161 datasets  
- **DANS Data Station Archaeology**: 162,435 datasets  
- **DANS SSH**: 7,932 datasets  
- **DANS Life Sciences**: 997 datasets  
- **DANS Physical & Technical Sciences**: 845 datasets  
- **IISH Dataverse**: 358 datasets  
- **ODISSEI Portal**: 10,163 datasets  

These are the major Dutch Dataverse nodes covering a wide range of research areas.

---

## 🌍 Node Growth Since 2015

Countries with the most new Dataverse nodes (2015–2025):

- 🇵�� **Poland**: 8+ new nodes
- 🇩🇪 Germany: 7+
- 🇧🇷 Brazil: 7+
- 🇺🇸 USA: 7+
- 🇫🇷 France: 6+
- ��🇹 Portugal: 5+
- 🇨🇴 Colombia: 5+
- 🇳🇱 Netherlands: 5+

> Poland leads in Dataverse expansion, with a surge of new nodes since 2023.

---

## 📘 Real-World Use Cases

### 1. 🔍 Discover Topics
**Q:** “How many datasets on *climate change* exist globally?”  
→ Use `search_datasets` across multiple hosts.

### 2. 🗺 Map Installations
**Q:** “Which countries added Dataverse installations since 2015?”  
→ Use `overview`, group by `country` and `created_at`.

### 3. 🧾 ML Metadata
Convert datasets to [Croissant ML](https://mlcroissant.org) format using `get_croissant_record`.

### 4. 📁 File Type Audits
Explore file formats in a dataset using `datatool`.

### 5. 📈 Regional Stats
Get dataset counts per year or per node using `overview_datasets`.

### 6. 🏛 Institutional Comparison
Compare dataset counts for institutions like Harvard vs. Johns Hopkins.

### 7. 🔗 Domain Linking
Combine datasets from different disciplines (e.g., linguistics + demographics).

### 8. 🧠 Dataset Recommendations
**Use Case:** "Gender inequality in education"
- Education Dataverse (CEM)
- UNESCO-UIS Education
- NCES (U.S. education stats)
- Politics & Gender Dataverse

Search using queries like `"gender gap education"`.

### 9. 🧺 Batch Processing
Download and convert all datasets in a topic using `search_datasets` + `get_croissant_record`.

### 10. 📊 Build Dashboards
Generate file-level stats from a host using `overview_files`.

---

## 📫 Need Help?

Open an issue or visit **https://mcp.dataverse.org**  
We’re happy to help you build intelligent agents and workflows on top of Dataverse!


