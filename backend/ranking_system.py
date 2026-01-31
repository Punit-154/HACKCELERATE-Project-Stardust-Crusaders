import json
import os
import pandas as pd
from collections import defaultdict
import logging
from datetime import datetime
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Set up logging for auditability
logging.basicConfig(filename='ranking_audit.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class EmissionsRankingSystem:
    def __init__(self, materials_file='sample_materials.csv', transport_file='sample_transport.csv'):
        self.materials_file = materials_file
        self.transport_file = transport_file
        self.materials_ranking = []
        self.transport_ranking = []
        self.last_update = None

    def load_materials_data(self):
        """Load materials data from CSV."""
        if not os.path.exists(self.materials_file):
            raise FileNotFoundError(f"Materials file {self.materials_file} not found.")
        return pd.read_csv(self.materials_file)

    def load_transport_data(self):
        """Load transport data from CSV."""
        if not os.path.exists(self.transport_file):
            raise FileNotFoundError(f"Transport file {self.transport_file} not found.")
        return pd.read_csv(self.transport_file)

    def calculate_materials_emissions(self, materials_df):
        """Calculate emissions for materials using calc_material_emissions.py logic."""
        # Simplified version for ranking system - using basic emission factors
        emission_factors = {
            'Steel': 1.85,  # kg CO2e per kg
            'Aluminum': 8.24,
            'Recycled Steel': 0.73,
            'Cement': 0.85,
            'Iron Wire': 2.0
        }

        results = []
        for idx, row in materials_df.iterrows():
            material = str(row['Material']).strip()
            weight = float(row['Weight'])
            unit = str(row['Unit']).lower().strip()
            entity = str(row['Entity']).strip()

            # Convert to kg
            if unit == 'kg':
                weight_kg = weight
            elif unit == 'g':
                weight_kg = weight / 1000
            elif unit in ['tons', 'tonnes']:
                weight_kg = weight * 1000
            elif unit == 'lbs':
                weight_kg = weight * 0.453592
            else:
                continue

            # Get emission factor
            factor = emission_factors.get(material, 0)
            emissions = weight_kg * factor

            results.append({
                "entity": entity,
                "category": "materials",
                "material": material,
                "weight_kg": round(weight_kg, 2),
                "emissions_kg_co2e": round(emissions, 4),
                "unit": "kg",
                "source_file": self.materials_file
            })

        return results

    def calculate_transport_emissions(self, transport_df):
        """Calculate emissions for transport using calc_transport_emissions.py logic."""
        # Simplified version for ranking system - using basic emission factors
        emission_factors = {
            'truck': 0.0001,  # kg CO2e per tonne-km
            'ship': 0.00002,
            'rail': 0.000015,
            'air': 0.0005
        }

        results = []
        for idx, row in transport_df.iterrows():
            product = str(row['Product']).strip()
            weight_lbs = float(row['Weight_lbs'])
            distance_miles = float(row['Distance_miles'])
            mode = str(row['Mode']).lower().strip()
            entity = str(row['Entity']).strip()

            # Convert to metric units
            weight_kg = weight_lbs * 0.453592
            distance_km = distance_miles * 1.60934
            tonne_km = (weight_kg / 1000) * distance_km

            # Get emission factor
            factor = emission_factors.get(mode, 0)
            emissions = tonne_km * factor

            results.append({
                "entity": entity,
                "category": "transport",
                "product": product,
                "mode": mode,
                "weight_kg": round(weight_kg, 2),
                "distance_km": round(distance_km, 2),
                "tonne_km": round(tonne_km, 4),
                "emissions_kg_co2e": round(emissions, 4),
                "unit": "kg",
                "source_file": self.transport_file
            })

        return results

    def compute_materials_ranking(self, materials_emissions):
        """Compute ranking for materials by total CO2e emissions."""
        material_totals = defaultdict(float)
        for item in materials_emissions:
            material_totals[item['material']] += item['emissions_kg_co2e']

        # Sort by emissions descending
        self.materials_ranking = sorted(material_totals.items(), key=lambda x: x[1], reverse=True)
        logging.info(f"Materials ranking updated: {self.materials_ranking}")

    def compute_transport_ranking(self, transport_emissions):
        """Compute ranking for transport modes by total CO2e emissions."""
        transport_totals = defaultdict(float)
        for item in transport_emissions:
            transport_totals[item['mode']] += item['emissions_kg_co2e']

        # Sort by emissions descending
        self.transport_ranking = sorted(transport_totals.items(), key=lambda x: x[1], reverse=True)
        logging.info(f"Transport ranking updated: {self.transport_ranking}")

    def update_rankings(self):
        """Update rankings from current data."""
        # Load raw data
        materials_df = self.load_materials_data()
        transport_df = self.load_transport_data()

        # Calculate emissions
        materials_emissions = self.calculate_materials_emissions(materials_df)
        transport_emissions = self.calculate_transport_emissions(transport_df)

        # Compute rankings
        self.compute_materials_ranking(materials_emissions)
        self.compute_transport_ranking(transport_emissions)

        self.last_update = datetime.now()
        logging.info("Rankings updated successfully.")

    def get_materials_ranking(self):
        """Get current materials ranking."""
        return self.materials_ranking

    def get_transport_ranking(self):
        """Get current transport ranking."""
        return self.transport_ranking

    def save_rankings_to_file(self):
        """Save rankings to JSON files for persistence."""
        rankings = {
            'materials': self.materials_ranking,
            'transport': self.transport_ranking,
            'last_update': self.last_update.isoformat() if self.last_update else None
        }
        with open('current_rankings.json', 'w') as f:
            json.dump(rankings, f, indent=4)
        logging.info("Rankings saved to file.")

if __name__ == "__main__":
    system = EmissionsRankingSystem()
    system.update_rankings()
    system.save_rankings_to_file()
    print("Materials Ranking:")
    for rank, (material, emissions) in enumerate(system.get_materials_ranking(), 1):
        print(f"{rank}. {material}: {emissions:.2f} kg CO2e")
    print("\nTransport Ranking:")
    for rank, (mode, emissions) in enumerate(system.get_transport_ranking(), 1):
        print(f"{rank}. {mode}: {emissions:.2f} kg CO2e")
