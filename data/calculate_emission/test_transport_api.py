"""
Test script to find correct ClimateQ emission factors for transport modes
"""
import requests
import json

API_KEY = "A5WYRXFHWS0PV43QFYVHQF34MR"
DATA_VERSION = "30.30"

# Test different activity IDs for ship, rail, and air freight
test_cases = [
    # Ship freight
    {
        "name": "Ship - Container",
        "activity_id": "sea_freight-vessel_type_container_ship-route_type_na-vessel_length_na-tonnage_na-fuel_source_na",
        "params": {"distance": 1000, "distance_unit": "km", "weight": 500, "weight_unit": "kg"}
    },
    # Rail freight
    {
        "name": "Rail",
        "activity_id": "freight_train-route_type_na-fuel_type_na",
        "params": {"distance": 1000, "distance_unit": "km", "weight": 500, "weight_unit": "kg"}
    },
    # Air freight
    {
        "name": "Air - International",
        "activity_id": "freight_flight-route_type_international-distance_na-weight_na-rf_na-method_na-aircraft_type_na-distance_uplift_na",
        "params": {"distance": 1000, "distance_unit": "km", "weight": 500, "weight_unit": "kg"}
    },
]

print("Testing ClimateQ Emission Factors for Transport")
print("=" * 60)

for test in test_cases:
    payload = {
        "emission_factor": {
            "activity_id": test["activity_id"],
            "data_version": DATA_VERSION
        },
        "parameters": test["params"]
    }
    
    try:
        response = requests.post(
            "https://api.climatiq.io/data/v1/estimate",
            json=payload,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            timeout=10
        )
        
        data = response.json()
        
        if response.status_code == 200:
            print(f"[OK] {test['name']}")
            print(f"  Activity ID: {test['activity_id']}")
            print(f"  Emissions: {data['co2e']:.4f} {data['co2e_unit']}")
        else:
            print(f"[ERROR] {test['name']}")
            print(f"  Error: {data.get('message', 'Unknown error')}")
    
    except Exception as e:
        print(f"[ERROR] {test['name']}")
        print(f"  Exception: {e}")
    
    print()
