"""
Emission Aggregator
Combines emissions from all sources and aggregates by entity
"""

import json
from pathlib import Path
from typing import Dict, List
from collections import defaultdict


class EmissionAggregator:
    """Aggregate emissions from multiple sources by entity"""
    
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]
        self.emissions_dir = self.base_dir / "data" / "emissions"
    
    def load_emission_data(self, category: str) -> List[Dict]:
        """Load emission data for a specific category"""
        file_path = self.emissions_dir / f"{category}_emissions.json"
        
        if not file_path.exists():
            print(f"[WARN] No emission data found for {category}")
            return []
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print(f"[LOAD] Loaded {len(data)} {category} emission records")
        return data
    
    def aggregate_by_entity(self) -> Dict[str, Dict]:
        """Aggregate all emissions by entity"""
        
        print("\n" + "="*60)
        print("AGGREGATING EMISSIONS BY ENTITY")
        print("="*60)
        
        # Load all emission data
        materials_data = self.load_emission_data('materials')
        transport_data = self.load_emission_data('transport')
        energy_data = self.load_emission_data('energy')
        
        # Aggregate by entity
        entity_emissions = defaultdict(lambda: {
            'entity': '',
            'total_emissions_kg_co2e': 0.0,
            'materials_emissions_kg_co2e': 0.0,
            'transport_emissions_kg_co2e': 0.0,
            'energy_emissions_kg_co2e': 0.0,
            'breakdown': {
                'materials': [],
                'transport': [],
                'energy': []
            }
        })
        
        # Process materials
        for record in materials_data:
            entity = record['entity']
            emissions = record['emissions_kg_co2e']
            
            entity_emissions[entity]['entity'] = entity
            entity_emissions[entity]['materials_emissions_kg_co2e'] += emissions
            entity_emissions[entity]['total_emissions_kg_co2e'] += emissions
            entity_emissions[entity]['breakdown']['materials'].append(record)
        
        # Process transport
        for record in transport_data:
            entity = record['entity']
            emissions = record['emissions_kg_co2e']
            
            entity_emissions[entity]['entity'] = entity
            entity_emissions[entity]['transport_emissions_kg_co2e'] += emissions
            entity_emissions[entity]['total_emissions_kg_co2e'] += emissions
            entity_emissions[entity]['breakdown']['transport'].append(record)
        
        # Process energy
        for record in energy_data:
            entity = record['entity']
            emissions = record['emissions_kg_co2e']
            
            entity_emissions[entity]['entity'] = entity
            entity_emissions[entity]['energy_emissions_kg_co2e'] += emissions
            entity_emissions[entity]['total_emissions_kg_co2e'] += emissions
            entity_emissions[entity]['breakdown']['energy'].append(record)
        
        # Round all values
        for entity_data in entity_emissions.values():
            entity_data['total_emissions_kg_co2e'] = round(entity_data['total_emissions_kg_co2e'], 4)
            entity_data['materials_emissions_kg_co2e'] = round(entity_data['materials_emissions_kg_co2e'], 4)
            entity_data['transport_emissions_kg_co2e'] = round(entity_data['transport_emissions_kg_co2e'], 4)
            entity_data['energy_emissions_kg_co2e'] = round(entity_data['energy_emissions_kg_co2e'], 4)
        
        # Convert to list
        aggregated_list = list(entity_emissions.values())
        
        # Save aggregated data
        output_path = self.emissions_dir / "aggregated_emissions.json"
        with open(output_path, 'w') as f:
            json.dump(aggregated_list, f, indent=4)
        
        print(f"\n[OK] Aggregated emissions for {len(aggregated_list)} entities")
        print(f"[SAVE] Saved to: {output_path}")
        
        return entity_emissions
    
    def get_summary(self, entity_emissions: Dict) -> None:
        """Print summary of aggregated emissions"""
        
        print("\n" + "="*60)
        print("EMISSION SUMMARY BY ENTITY")
        print("="*60)
        
        for entity, data in sorted(entity_emissions.items()):
            print(f"\n{entity}:")
            print(f"  Total Emissions: {data['total_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"    Materials: {data['materials_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"    Transport: {data['transport_emissions_kg_co2e']:.2f} kg CO2e")
            print(f"    Energy: {data['energy_emissions_kg_co2e']:.2f} kg CO2e")


def aggregate_emissions():
    """Main function to aggregate emissions"""
    aggregator = EmissionAggregator()
    entity_emissions = aggregator.aggregate_by_entity()
    aggregator.get_summary(entity_emissions)
    return entity_emissions


if __name__ == "__main__":
    aggregate_emissions()
