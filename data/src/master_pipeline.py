"""
Master Pipeline
Orchestrates the entire carbon emission calculation workflow
"""

import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "calculate_emission"))

from calc_material_emissions import calculate_material_emissions
from calc_transport_emissions import calculate_transport_emissions
from calc_energy_emissions import calculate_energy_emissions
from emission_aggregator import aggregate_emissions
from generate_report import generate_reports


def run_pipeline():
    """Execute the complete emission calculation pipeline"""
    
    print("\n" + "="*70)
    print("UNIVERSAL CARBON EMISSION CALCULATION PIPELINE")
    print("="*70 + "\n")
    
    # Step 1: Calculate material emissions
    print("\n" + ">"*60)
    print("STEP 1: Calculating Material Emissions")
    print(">"*60)
    try:
        materials_results = calculate_material_emissions()
        print(f"[OK] Material emissions calculated: {len(materials_results)} records")
    except Exception as e:
        print(f"[ERROR] Error calculating material emissions: {e}")
        materials_results = []
    
    # Step 2: Calculate transport emissions
    print("\n" + ">"*60)
    print("STEP 2: Calculating Transport Emissions")
    print(">"*60)
    try:
        transport_results = calculate_transport_emissions()
        print(f"[OK] Transport emissions calculated: {len(transport_results)} records")
    except Exception as e:
        print(f"[ERROR] Error calculating transport emissions: {e}")
        transport_results = []
    
    # Step 3: Calculate energy emissions
    print("\n" + ">"*60)
    print("STEP 3: Calculating Energy Emissions")
    print(">"*60)
    try:
        energy_results = calculate_energy_emissions()
        print(f"[OK] Energy emissions calculated: {len(energy_results)} records")
    except Exception as e:
        print(f"[ERROR] Error calculating energy emissions: {e}")
        energy_results = []
    
    # Step 4: Aggregate emissions by entity
    print("\n" + ">"*60)
    print("STEP 4: Aggregating Emissions by Entity")
    print(">"*60)
    try:
        entity_emissions = aggregate_emissions()
        print(f"[OK] Emissions aggregated for {len(entity_emissions)} entities")
    except Exception as e:
        print(f"[ERROR] Error aggregating emissions: {e}")
        entity_emissions = {}
    
    # Step 5: Generate reports
    print("\n" + ">"*60)
    print("STEP 5: Generating Reports")
    print(">"*60)
    try:
        top_5, summary = generate_reports()
        print(f"[OK] Reports generated successfully")
    except Exception as e:
        print(f"[ERROR] Error generating reports: {e}")
        top_5, summary = [], {}
    
    # Final summary
    print("\n" + "="*70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    
    print(f"\nTotal Records Processed:")
    print(f"  - Materials: {len(materials_results)}")
    print(f"  - Transport: {len(transport_results)}")
    print(f"  - Energy: {len(energy_results)}")
    print(f"  - Entities: {len(entity_emissions)}")
    
    if summary:
        print(f"\nOverall Statistics:")
        print(f"  - Total Emissions: {summary.get('total_emissions_kg_co2e', 0):.2f} kg CO2e")
        print(f"  - Average per Entity: {summary.get('average_emissions_kg_co2e', 0):.2f} kg CO2e")
    
    print(f"\n>> Check the 'data/reports' directory for detailed reports!")
    
    return {
        'materials': materials_results,
        'transport': transport_results,
        'energy': energy_results,
        'aggregated': entity_emissions,
        'top_5_lowest': top_5,
        'summary': summary
    }


if __name__ == "__main__":
    run_pipeline()
