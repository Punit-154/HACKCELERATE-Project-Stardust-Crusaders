"""
Transport Emissions Calculator
Calculates carbon emissions from freight transport activities
"""

import requests
import json
from pathlib import Path
import sys

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from universal_data_loader import UniversalDataLoader # type: ignore


def calculate_transport_emissions():
    """Calculate emissions for all transport activities"""
    
    # Initialize data loader
    loader = UniversalDataLoader()
    
    print("="*60)
    print("TRANSPORT EMISSIONS CALCULATION")
    print("="*60)
    
    transport_df = loader.load_data_source('transport')
    
    if transport_df.empty:
        print("[ERROR] No transport data found")
        return []
    
    # Get configuration
    schema = loader.get_schema('transport')
    emission_factors = loader.get_emission_factors('transport')
    api_config = loader.get_api_config()
    
    # Get allowed transport modes and intermodal config
    config = loader.config
    allowed_modes = config.get('allowed_transport_modes', [])
    intermodal_config = config.get('intermodal_config', {})
    intermodal_enabled = intermodal_config.get('enabled', False)
    leg_distribution = intermodal_config.get('default_leg_distribution', {})
    
    print(f"[INFO] Filtering for allowed transport modes: {', '.join(allowed_modes)}")
    if intermodal_enabled:
        print(f"[INFO] Intermodal distance estimation enabled")
    
    # Extract field names from schema
    entity_field = schema.get('entity_field', 'Entity')
    product_field = schema.get('product_field', 'Product')
    weight_field = schema.get('weight_field', 'Weight_lbs')
    distance_field = schema.get('distance_field', 'Distance_miles')
    mode_field = schema.get('mode_field', 'Mode')
    
    results = []
    
    for idx, row in transport_df.iterrows():
        entity = row.get(entity_field, 'Unknown')
        product = row.get(product_field, 'Unknown')
        weight_lbs = float(row[weight_field])
        distance_miles = float(row[distance_field])
        mode = row[mode_field].lower()
        
        # Filter: Only process allowed transport modes
        if allowed_modes and mode not in allowed_modes:
            continue
        
        # Convert to metric units
        weight_kg = weight_lbs * 0.453592
        distance_km = distance_miles * 1.60934
        
        # Check if intermodal estimation is needed
        # If mode is 'intermodal' or if intermodal is enabled, calculate multi-leg emissions
        if intermodal_enabled and mode == 'intermodal':
            # Calculate emissions for each leg
            total_emissions = 0
            leg_details = []
            
            for leg_mode, proportion in leg_distribution.items():
                if leg_mode not in allowed_modes:
                    continue
                    
                leg_distance_km = distance_km * proportion
                leg_tonne_km = (weight_kg / 1000) * leg_distance_km
                
                activity_id = emission_factors.get(leg_mode)
                if not activity_id:
                    continue
                
                # API call for this leg
                payload = {
                    "emission_factor": {
                        "activity_id": activity_id,
                        "data_version": api_config['data_version']
                    },
                    "parameters": {
                        "distance": leg_distance_km,
                        "distance_unit": "km",
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
                        leg_emissions = data['co2e']
                        total_emissions += leg_emissions
                        leg_details.append({
                            "mode": leg_mode,
                            "distance_km": round(leg_distance_km, 2),
                            "proportion": proportion,
                            "emissions_kg_co2e": round(leg_emissions, 4)
                        })
                        print(f"  [LEG] {leg_mode} ({leg_distance_km:.2f} km, {proportion*100:.0f}%) -> {leg_emissions:.2f} kg CO2e")
                    else:
                        print(f"[ERROR] API Error for {leg_mode} leg: {data}")
                
                except Exception as e:
                    print(f"[ERROR] Exception for {leg_mode} leg: {e}")
            
            # Store intermodal result
            if leg_details:
                emission_result = {
                    "entity": entity,
                    "category": "transport",
                    "product": product,
                    "mode": "intermodal",
                    "weight_kg": round(weight_kg, 2),
                    "distance_km": round(distance_km, 2),
                    "emissions_kg_co2e": round(total_emissions, 4),
                    "unit": "kg",
                    "legs": leg_details,
                    "source_file": row.get('_source_file', 'unknown')
                }
                results.append(emission_result)
                print(f"[OK] {entity} - {product} via intermodal ({distance_km:.2f} km) -> {total_emissions:.2f} kg CO2e")
            
            continue
        
        # Single-mode transport calculation
        tonne_km = (weight_kg / 1000) * distance_km
        
        # Get activity ID for this transport mode
        activity_id = emission_factors.get(mode)
        
        if not activity_id:
            continue
        
        # Prepare API request
        payload = {
            "emission_factor": {
                "activity_id": activity_id,
                "data_version": api_config['data_version']
            },
            "parameters": {
                "distance": distance_km,
                "distance_unit": "km",
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
                    "category": "transport",
                    "product": product,
                    "mode": mode,
                    "weight_kg": round(weight_kg, 2),
                    "distance_km": round(distance_km, 2),
                    "tonne_km": round(tonne_km, 4),
                    "emissions_kg_co2e": round(data['co2e'], 4),
                    "unit": data['co2e_unit'],
                    "source_file": row.get('_source_file', 'unknown')
                }
                results.append(emission_result)
                print(f"[OK] {entity} - {product} via {mode} ({tonne_km:.2f} t*km) -> {data['co2e']:.2f} kg CO2e")
            else:
                print(f"[ERROR] API Error for {product} via {mode}: {data}")
        
        except Exception as e:
            print(f"[ERROR] Exception for {product} via {mode}: {e}")
    
    # Save results
    # Save results
    output_config = config.get('output', {})
    emissions_dir = output_config.get('emissions_dir', '.')
    
    # If using loader from same dir, emissions_dir might be relative to script
    output_path = Path(emissions_dir) / "transport_emissions.json"
    
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n[TRANSPORT] Transport emissions saved to: {output_path}")
    print(f"Total records: {len(results)}")
    
    return results


if __name__ == "__main__":
    calculate_transport_emissions()
