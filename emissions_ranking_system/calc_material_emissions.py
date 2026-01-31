"""
Enhanced Material Emissions Calculator
Uses universal data loader and supports entity tracking
"""

import requests
import json
from pathlib import Path
from universal_data_loader import UniversalDataLoader # type: ignore


def calculate_material_emissions():
    """Calculate emissions for all materials from universal data sources"""
    
    # Initialize data loader
    loader = UniversalDataLoader()
    
    # Load materials data
    print("="*60)
    print("MATERIAL EMISSIONS CALCULATION")
    print("="*60)
    
    materials_df = loader.load_data_source('materials')
    
    if materials_df.empty:
        print("[ERROR] No materials data found")
        return []
    
    # Get configuration
    schema = loader.get_schema('materials')
    emission_factors = loader.get_emission_factors('materials')
    api_config = loader.get_api_config()
    
    # Get allowed materials list
    config = loader.config
    allowed_materials = config.get('allowed_materials', [])
    
    
    
    # Extract field names from schema
    entity_field = schema.get('entity_field', 'Entity')
    material_field = schema.get('material_field', 'Material')
    weight_field = schema.get('weight_field', 'Weight')
    unit_field = schema.get('unit_field', 'Unit')
    
    results = []
    
    for idx, row in materials_df.iterrows():
        material = row[material_field]
        
        # Filter: Only process allowed materials
        if allowed_materials and material not in allowed_materials:
            
            continue
        
        weight = float(row[weight_field])
        unit = row[unit_field].lower()
        entity = row.get(entity_field, 'Unknown')
        
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
        
        # Get activity ID for this material
        activity_id = emission_factors.get(material)
        
        if not activity_id:
            continue
        
        # Prepare API request
        payload = {
            "emission_factor": {
                "activity_id": activity_id,
                "data_version": api_config['data_version']
            },
            "parameters": {
                "weight": weight_kg,
                "weight_unit": "kg"
            }
        }
        
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
                    "category": "materials",
                    "material": material,
                    "weight_kg": round(weight_kg, 2),
                    "emissions_kg_co2e": round(data['co2e'], 4),
                    "unit": data['co2e_unit'],
                    "source_file": row.get('_source_file', 'unknown')
                }
                results.append(emission_result)
                print(f"[OK] {entity} - {material} ({weight_kg:.2f} kg) -> {data['co2e']:.2f} kg CO2e")
            else:
                print(f"[ERROR] API Error for {material}: {data}")
        
        except Exception as e:
            print(f"[ERROR] Exception for {material}: {e}")
    
    # Save results
    output_config = config.get('output', {})
    emissions_dir = output_config.get('emissions_dir', '.')
    
    output_path = Path(emissions_dir) / "materials_emissions.json"
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n[SAVE] Material emissions saved to: {output_path}")
    print(f"Total records: {len(results)}")
    
    return results


if __name__ == "__main__":
    calculate_material_emissions()
