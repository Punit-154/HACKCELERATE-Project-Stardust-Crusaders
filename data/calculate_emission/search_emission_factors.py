"""
Search for correct ClimateQ emission factors
"""
import requests
import json

API_KEY = "A5WYRXFHWS0PV43QFYVHQF34MR"

# Search for freight emission factors
search_terms = ["sea freight", "rail freight", "air freight"]

print("Searching for ClimateQ Emission Factors")
print("=" * 60)

for term in search_terms:
    print(f"\nSearching for: {term}")
    print("-" * 40)
    
    try:
        response = requests.get(
            "https://api.climatiq.io/data/v1/search",
            params={
                "query": term,
                "category": "Freight",
                "year": "2024"
            },
            headers={
                "Authorization": f"Bearer {API_KEY}"
            },
            timeout=10
        )
        
        data = response.json()
        
        if response.status_code == 200 and "results" in data:
            results = data["results"][:5]  # Show first 5 results
            print(f"Found {len(data['results'])} results (showing first 5):")
            for i, result in enumerate(results, 1):
                print(f"\n  {i}. {result.get('name', 'N/A')}")
                print(f"     ID: {result.get('activity_id', 'N/A')}")
                print(f"     Unit: {result.get('unit_type', 'N/A')}")
                print(f"     Source: {result.get('source', 'N/A')}")
        else:
            print(f"  Error: {data.get('message', 'Unknown error')}")
    
    except Exception as e:
        print(f"  Exception: {e}")
