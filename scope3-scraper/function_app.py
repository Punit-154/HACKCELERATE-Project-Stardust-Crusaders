import azure.functions as func
import logging
import json
import os
import re
import csv
import io
from datetime import datetime
from azure.storage.blob import BlobServiceClient
from playwright.async_api import async_playwright
from openai import AsyncAzureOpenAI

app = func.FunctionApp()

# --- HELPER: Ask GPT-4 to find the data ---
async def extract_emissions_with_llm(text_content, company_name):
    client = AsyncAzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_KEY"),
        api_version="2024-02-15-preview" # KEPT EXACTLY AS YOU HAD IT
    )

    prompt = f"""
    Analyze the following text from {company_name}'s sustainability report.
    Extract the 'Scope 3' carbon emissions data.
    Return ONLY a valid JSON object. Do not add markdown formatting.
    
    Required JSON Structure:
    {{
        "company_name": "{company_name}",
        "reporting_year": "Int (e.g. 2023)",
        "total_scope_3_mtco2e": "Float (in Million Tonnes)",
        "categories": [
            {{"name": "Category Name (e.g. Purchased Goods)", "value": "Float"}}
        ]
    }}

    Text content to analyze (truncated):
    {text_content[:15000]} 
    """

    response = await client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        messages=[{"role": "system", "content": "You are a sustainability data expert."},
                  {"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    # Clean up the response (remove ```json wrappers if the AI adds them)
    raw_content = response.choices[0].message.content
    clean_json = raw_content.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)

# --- NEW HELPER: Convert JSON to CSV String ---
def json_to_csv_string(json_data):
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['Company', 'Year', 'Total_Scope3_MTCO2e', 'Category', 'Category_Emissions_MTCO2e', 'Scraped_Date'])
    
    company = json_data.get('company_name', 'Unknown')
    year = json_data.get('reporting_year', 'Unknown')
    total = json_data.get('total_scope_3_mtco2e', 0)
    scrape_date = datetime.now().strftime("%Y-%m-%d")
    
    # Rows
    categories = json_data.get('categories', [])
    if categories:
        for cat in categories:
            writer.writerow([
                company, 
                year, 
                total, 
                cat.get('name', 'Unknown'), 
                cat.get('value', 0),
                scrape_date
            ])
    else:
        writer.writerow([company, year, total, "Total Only", total, scrape_date])
        
    return output.getvalue()

# --- MAIN FUNCTION ---
@app.route(route="ScrapeScope3", auth_level=func.AuthLevel.ANONYMOUS)
async def ScrapeScope3(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Starting Smart Scraper (CSV Mode)...')

    company_name = req.params.get('company_name')
    if not company_name:
        return func.HttpResponse("Please provide ?company_name=...", status_code=400)
    
    try:
        # 1. Start Browser
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # 2. Simulation Logic (KEPT YOUR EXACT TEXT)
            fake_pdf_text = ""
            if company_name.lower() == "tesla":
                fake_pdf_text = """
                Tesla 2023 Impact Report. 
                Scope 3 Emissions: Supply Chain emissions were 30.1 Million Metric Tonnes CO2e.
                Use of Sold Products: 21.5 Million Tonnes.
                Purchased Goods and Services: 8.2 Million Tonnes.
                """
            elif company_name.lower() == "apple":
                fake_pdf_text = """
                Apple Environmental Progress Report 2024.
                Total Scope 3 emissions: 15.4 million metric tons CO2e.
                Manufacturing: 9.4 million tons.
                Product Transport: 1.2 million tons.
                Product Use: 3.8 million tons.
                """
            else:
                fake_pdf_text = f"No pre-loaded data found for {company_name}. Please use Tesla or Apple for the demo."

            # 3. AI Extraction
            logging.info("Sending text to Azure OpenAI...")
            ai_result = await extract_emissions_with_llm(fake_pdf_text, company_name)
            
            # 4. Convert to CSV (NEW)
            csv_data = json_to_csv_string(ai_result)
            
            # 5. Save CSV to Azure
            connect_str = os.getenv('AzureWebJobsStorage')
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)
            container_name = "raw-zone"
            
            # Changed filename to .csv
            file_name = f"{company_name}_scope3_live.csv"
            
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
            blob_client.upload_blob(csv_data, overwrite=True)
            
            logging.info(f"Uploaded {file_name} to Azure.")
            
            # 6. Return CSV to Browser
            return func.HttpResponse(
                csv_data,
                mimetype="text/csv",
                status_code=200
            )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)