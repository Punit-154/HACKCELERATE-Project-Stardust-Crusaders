# HACKCELERATE-Project-Stardust-Crusaders
Hacakthon Sustainable Track

# 🌍 Dynamic Carbon Intelligence Platform
### *Beyond Static Estimation: AI-Powered Scope 3 Emission Tracking & Optimization*

![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![NodeJS](https://img.shields.io/badge/node.js-6DA55F?style=for-the-badge&logo=node.js&logoColor=white)
![OpenAI](https://img.shields.io/badge/Azure%20OpenAI-412991.svg?style=for-the-badge&logo=openai&logoColor=white)

## 📖 Executive Summary
Scope 3 emissions (supply chain) account for ~90% of a company's carbon footprint but are notoriously difficult to track due to fragmented data. Current solutions rely on "spend-based" averages (e.g., $1 spend = 1kg CO2), which leads to greenwashing.

**Our Solution:** An **Audit-Ready Carbon Intelligence System** that ingests primary data (invoices, logistics logs), maps them to scientific emission factors (Climatiq/EPA), and uses a **Dual-Pipeline RAG Architecture** to not only *measure* carbon but *optimize* it.

---

## 🏗 System Architecture

We utilize a **Two-Pipeline Approach** powered by Microsoft Azure.

### 🔄 Pipeline 1: The "Visibility" Engine (RAG & Ingestion)
*Goal: Ingest messy raw data and normalize it into a queryable "Single Source of Truth."*

1.  **Data Injection (Azure Blob Storage):**
    * Raw data (Excel/CSV procurement logs, PDF invoices) is uploaded to an Azure Blob Container (`raw-zone`).
    * **Azure Data Factory (ADF)** triggers an ETL pipeline to clean and normalize units (e.g., converting "gallons" to "liters").
2.  **Vectorization (Azure AI Search):**
    * Processed data is indexed by **Azure AI Search**.
    * We use hybrid search (Keyword + Vector) to make the supply chain data "talkable."
3.  **Intelligence (Azure OpenAI):**
    * **GPT-4o** is connected to the search index.
    * Users can ask natural language questions: *"Which supplier contributed the most to our Q3 emissions?"*

### 📉 Pipeline 2: The "Optimization" Engine (Recommendation)
*Goal: actively reduce the footprint using AI.*

1.  **Hotspot Analysis:** The system identifies high-emission nodes (e.g., Air Freight vs. Sea Freight).
2.  **Substitution logic:**
    * The engine queries our database of **Emission Factors** (via Climatiq API).
    * It simulates scenarios: *"Switching Route A to Rail would save 40 tons of CO2e."*
3.  **Output:** Actionable, audit-ready recommendations for procurement teams.

---

## 🛠 Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Node.js, Express, React | User Dashboard & Interaction |
| **LLM Orchestration** | **Azure OpenAI Service** | Natural Language Processing & Reasoning |
| **Vector DB** | **Azure AI Search** | Indexing Supply Chain Data for RAG |
| **Storage** | **Azure Blob Storage** | Data Lake for raw CSV/PDFs |
| **ETL** | **Azure Data Factory** | Data Transformation & Cleaning |
| **Carbon Data** | **Climatiq API** | Scientific Emission Factor Mapping |

---

## 🚀 Installation & Setup

### Prerequisites
* Node.js (v18+)
* Azure Subscription (OpenAI & AI Search enabled)
* Climatiq API Key

### 1. Clone the Repository
```bash
git clone [https://github.com/your-team/carbon-intelligence.git](https://github.com/your-team/carbon-intelligence.git)
cd carbon-intelligence
