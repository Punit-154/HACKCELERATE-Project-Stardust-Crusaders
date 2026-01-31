import pandas as pd
import json
from pathlib import Path

# -----------------------------
# PATH SETUP
# -----------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = BASE_DIR / "data" / "raw" / "sample_materials.csv"
OUTPUT_PATH = BASE_DIR / "data" / "cleaned" / "materials.json"

# Create processed folder if it doesn't exist
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------
# LOAD CSV
# -----------------------------
print("Reading materials CSV...")
df = pd.read_csv(RAW_DATA_PATH)

print("Raw Data:")
print(df)

# -----------------------------
# CLEAN & STANDARDIZE
# -----------------------------
df.columns = df.columns.str.strip()  # remove space issues

materials_list = []

for _, row in df.iterrows():
    material = row["Material"]
    weight = float(row["Weight"])
    unit = row["Unit"].lower()

    # Convert to kg if needed
    if unit == "kg":
        weight_kg = weight
    elif unit == "g":
        weight_kg = weight / 1000
    elif unit == "tons":
        weight_kg = weight * 1000
    else:
        print(f"Unknown unit for {material}, skipping...")
        continue

    materials_list.append({
        "material": material,
        "weight_kg": weight_kg,
        "source": row["Source"]
    })

# -----------------------------
# SAVE TO JSON
# -----------------------------
with open(OUTPUT_PATH, "w") as f:
    json.dump(materials_list, f, indent=4)

print("\n[OK] Processed materials saved to:", OUTPUT_PATH)
print("Preview:", materials_list[:2])
