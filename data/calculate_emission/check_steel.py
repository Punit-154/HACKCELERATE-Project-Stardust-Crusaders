import requests
import json

API_KEY = "A5WYRXFHWS0PV43QFYVHQF34MR"

url = "https://api.climatiq.io/data/v1/search"

params = {
    "query": "ship",                 # simpler keyword
    "category": "Sea Freight",    # sometimes "Transport" works too
    "sector": "Transport",
    "unit_type": "WeightOverDistance",  # correct for freight
    "data_version": "^23",
    "results_per_page": 5
}



response = requests.get(
    url,
    headers={"Authorization": f"Bearer {API_KEY}"},
    params=params
)

data = response.json()

print("Status Code:", response.status_code)

if "results" in data:
    for item in data["results"]:
        print("\nNAME:", item["name"])
        print("ID:", item["activity_id"])
        print("UNIT:", item["unit_type"])
        print("REGION:", item["region"])
else:
    pprint(json.dumps(data, indent=4))

