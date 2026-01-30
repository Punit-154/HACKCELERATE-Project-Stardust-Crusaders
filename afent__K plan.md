# ⚔️ Operation Carbon Intelligence: ETL & RAG Pipeline
### *The Backbone Strategy for Hackathon Victory*

![Status](https://img.shields.io/badge/Status-MISSION%20CRITICAL-red?style=for-the-badge)
![Azure](https://img.shields.io/badge/Azure-Data_Factory-0078D4?style=for-the-badge&logo=azure-data-factory&logoColor=white)
![AI](https://img.shields.io/badge/AI-Azure_OpenAI-5e9693?style=for-the-badge&logo=openai&logoColor=white)

---

## 🎯 Objective
**Goal:** Build an automated pipeline that ingests messy raw data, cleans it (unit normalization), and feeds it into a Vector Search index for GPT-4 to query.

**Timeline:** 60 Minutes
**Priority:** High

---

## 1️⃣ Phase 1: Storage Setup (The Landing Zone)
*Goal: Segregate "Dirty" Raw Data from "Clean" AI-Ready Data.*

- [ ] **Navigate to:** Azure Portal → Storage Accounts.
- [ ] **Action:** Create two containers inside your storage account.
    - 📂 `raw-zone`: Upload your messy Excel (`.xlsx`) or CSV files here.
    - 📂 `curated-zone`: **Leave Empty.** This is the destination for clean data.

---

## 2️⃣ Phase 2: The "Cleaning" Pipeline (Azure Data Factory)
*Goal: The Machine that turns "Gallons" into "Liters".*

### A. Infrastructure
1.  **Create Service:** Search "Data factories" → Create `carbon-etl-factory`.
2.  **Launch Studio:** Open the ADF Studio UI.

### B. Connect Data (Datasets)
- [ ] **Source Dataset:**
    - `Author` → `Dataset` (+) → `Azure Blob Storage` → `CSV`.
    - **Point to:** `raw-zone` container.
- [ ] **Sink Dataset:**
    - `Author` → `Dataset` (+) → `Azure Blob Storage` → `CSV`.
    - **Point to:** `curated-zone` container.

### C. The Logic (Mapping Data Flow)
1.  **Create Flow:** Right-click `Data flows` → `New data flow`.
2.  **Add Source:** Select your `raw-zone` dataset.
3.  **Add Derived Column (The Math):**
    - Click `+` on source node → Search **"Derived Column"**.
    - **Column Name:** `Normalized_Volume_Liters`
    - **Expression:**
    ```sql
    case(
        Unit == 'gallons', Quantity * 3.785,
        Unit == 'liters', Quantity,
        0.0
    )
    ```
4.  **Add Sink:** Connect to the Derived Column → Select `curated-zone` dataset.

### D. Execute
- [ ] **Create Pipeline:** Drag your Data Flow onto the canvas.
- [ ] **Debug Run:** Click `Debug`.
- [ ] **Verify:** Go to Storage Browser → `curated-zone`. *Do you see a new file with fixed numbers?*

---

## 3️⃣ Phase 3: Vectorization (Azure AI Search)
*Goal: Index the CLEAN data, ignore the raw mess.*

- [ ] **Navigate to:** Azure AI Search Resource.
- [ ] **Action:** Click **"Import Data"**.
- [ ] **Data Source:** Azure Blob Storage.
    - 🚨 **CRITICAL:** Select the **`curated-zone`** container.
- [ ] **Index Configuration:**
    - **Name:** `carbon-clean-index`
    - **Fields:** Set `Supplier`, `Material`, and `Normalized_Volume_Liters` to **Retrievable** & **Searchable**.
- [ ] **Run Indexer:** Submit and wait for "Success".

---

## 4️⃣ Phase 4: Intelligence (Node.js + OpenAI)
*Goal: Force the AI to use your calculated math.*

### A. Update Environment
Update your `.env` file to point to the new clean index.
```bash
AZURE_SEARCH_INDEX="carbon-clean-index"
