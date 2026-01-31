import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_FILE = BASE_DIR / "data" / "raw" / "sample_transport.csv"
OUTPUT_FILE = BASE_DIR / "data" / "cleaned" / "transport.json"

df = pd.read_csv(INPUT_FILE)

transport_list = []

for _, row in df.iterrows():
    # Convert units
    weight_kg = row["Weight_lbs"] * 0.453592
    distance_km = row["Distance_miles"] * 1.60934

    tonne_km = (weight_kg / 1000) * distance_km

    transport_list.append({
        "product": row["Product"],
        "origin": row["Origin"],
        "destination": row["Destination"],
        "mode": row["Mode"].lower(),  # truck/ship
        "weight_kg": round(weight_kg, 2),
        "distance_km": round(distance_km, 2),
        "tonne_km": round(tonne_km, 2)
    })

# Ensure processed folder exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    json.dump(transport_list, f, indent=4)

print("[TRANSPORT] Transport data cleaned & saved to:", OUTPUT_FILE)
