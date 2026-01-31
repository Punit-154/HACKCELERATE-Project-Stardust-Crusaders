"""
Energy Emissions Calculator
Calculates carbon emissions from energy consumption
"""

import requests
import json
from pathlib import Path
import sys

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from universal_data_loader import UniversalDataLoader


def calculate_energy_emissions():
    """Calculate emissions for all energy consumption"""
    
    # Initialize data loader
    loader = UniversalDataLoader()
    
    print("="*60)
    print("ENERGY EMISSIONS CALCULATION")
    print("="*60)
    
    energy_df = loader.load_data_source('energy')
    
    if energy_df.empty:
        print("[ERROR] No energy data found")
        return []
    
    # Get configuration
    schema = loader.get_schema('energy')
    emission_factors = loader.get_emission_factors('energy')
    api_config = loader.get_api_config()
    
    # Extract field names from schema
    entity_field = schema.get('entity_field', 'Entity')
    energy_type_field = schema.get('energy_type_field', 'EnergyType')
    consumption_field = schema.get('consumption_field', 'Consumption')
    unit_field = schema.get('unit_field', 'Unit')
    location_field = schema.get('location_field', 'Location')
    
    results = []
    
    for idx, row in energy_df.iterrows():
        entity = row.get(entity_field, 'Unknown')
        energy_type = row[energy_type_field]
        consumption = float(row[consumption_field])
        unit = row[unit_field].lower()
        location = row.get(location_field, 'Unknown')
        
        # Get activity ID for this energy type
        energy_key = energy_type.lower().replace(' ', '_')
        activity_id = emission_factors.get(energy_key)
        
        if not activity_id:
            print(f"[WARN] No emission factor for energy type '{energy_type}', skipping...")
            continue
        
        # Prepare parameters based on energy type
        if energy_type.lower() == 'electricity':
            # Electricity in kWh
            if unit in ['kwh', 'kilowatt-hour', 'kilowatt-hours']:
                energy_value = consumption
                energy_unit = 'kWh'
            elif unit in ['mwh', 'megawatt-hour', 'megawatt-hours']:
                energy_value = consumption * 1000
                energy_unit = 'kWh'
            else:
                print(f"[WARN] Unknown electricity unit '{unit}', skipping...")
                continue
            
            payload = {
                "emission_factor": {
                    "activity_id": activity_id,
                    "data_version": api_config['data_version']
                },
                "parameters": {
                    "energy": energy_value,
                    "energy_unit": energy_unit
                }
            }
        
        elif energy_type.lower() == 'natural gas':
            # Natural gas in m3 or volume
            if unit in ['m3', 'cubic_meter', 'cubic_meters']:
                volume_value = consumption
                volume_unit = 'm3'
            else:
                print(f"[WARN] Unknown natural gas unit '{unit}', skipping...")
                continue
            
            payload = {
                "emission_factor": {
                    "activity_id": activity_id,
                    "data_version": api_config['data_version']
                },
                "parameters": {
                    "volume": volume_value,
                    "volume_unit": volume_unit
                }
            }
        
        elif energy_type.lower() in ['diesel', 'gasoline']:
            # Fuel in liters
            if unit in ['liters', 'liter', 'l']:
                volume_value = consumption
                volume_unit = 'l'
            elif unit in ['gallons', 'gallon', 'gal']:
                volume_value = consumption * 3.78541
                volume_unit = 'l'
            else:
                print(f"[WARN] Unknown fuel unit '{unit}', skipping...")
                continue
            
            payload = {
                "emission_factor": {
                    "activity_id": activity_id,
                    "data_version": api_config['data_version']
                },
                "parameters": {
                    "volume": volume_value,
                    "volume_unit": volume_unit
                }
            }
        
        else:
            print(f"[WARN] Unsupported energy type '{energy_type}', skipping...")
            continue
        
        try:
            response = requests.post(
                "https://api.climatiq.io/data/v1/estimate",
                json=payload,
                headers={
                    "Authorization": f"Bearer {api_config['climatiq_api_key']}",
                    "Content-Type": "application/json"
                },
                timeout=20
            )
            
            data = response.json()
            
            if response.status_code == 200:
                emission_result = {
                    "entity": entity,
                    "category": "energy",
                    "energy_type": energy_type,
                    "consumption": consumption,
                    "consumption_unit": unit,
                    "location": location,
                    "emissions_kg_co2e": round(data['co2e'], 4),
                    "unit": data['co2e_unit'],
                    "source_file": row.get('_source_file', 'unknown')
                }
                results.append(emission_result)
                print(f"[OK] {entity} - {energy_type} ({consumption} {unit}) -> {data['co2e']:.2f} kg CO2e")
            else:
                print(f"[ERROR] API Error for {energy_type}: {data}")
        
        except Exception as e:
            print(f"[ERROR] Exception for {energy_type}: {e}")
    
    # Save results
    base_dir = Path(__file__).resolve().parents[2]
    output_dir = base_dir / "data" / "emissions"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / "energy_emissions.json"
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n[ENERGY] Energy emissions saved to: {output_path}")
    print(f"Total records: {len(results)}")
    
    return results


if __name__ == "__main__":
    calculate_energy_emissions()
