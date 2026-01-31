"""
Test Script for Emissions Calculation System
Runs material and transport emissions calculations and displays results
"""

import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

print("=" * 70)
print("EMISSIONS CALCULATION SYSTEM - TEST SCRIPT")
print("=" * 70)
print()

# Test 1: Material Emissions
print("TEST 1: Material Emissions Calculation")
print("-" * 70)
try:
    from calc_material_emissions import calculate_material_emissions
    
    material_results = calculate_material_emissions()
    
    print(f"\n[SUCCESS] Material emissions calculated successfully!")
    print(f"Total records processed: {len(material_results)}")
    
    if material_results:
        print("\nSample results:")
        for i, result in enumerate(material_results[:3], 1):
            print(f"  {i}. {result['entity']} - {result['material']}: "
                  f"{result['emissions_kg_co2e']:.2f} kg CO2e")
    
except Exception as e:
    print(f"[ERROR] Material emissions test failed: {e}")

print("\n" + "=" * 70)
print()

# Test 2: Transport Emissions
print("TEST 2: Transport Emissions Calculation")
print("-" * 70)
try:
    from calc_transport_emissions import calculate_transport_emissions
    
    transport_results = calculate_transport_emissions()
    
    print(f"\n[SUCCESS] Transport emissions calculated successfully!")
    print(f"Total records processed: {len(transport_results)}")
    
    if transport_results:
        print("\nSample results:")
        for i, result in enumerate(transport_results[:3], 1):
            mode_info = f"via {result['mode']}"
            if result['mode'] == 'intermodal':
                mode_info += f" ({len(result.get('legs', []))} legs)"
            print(f"  {i}. {result['entity']} - {result['product']} {mode_info}: "
                  f"{result['emissions_kg_co2e']:.2f} kg CO2e")
    
except Exception as e:
    print(f"[ERROR] Transport emissions test failed: {e}")

print("\n" + "=" * 70)
print()

# Summary
print("TEST SUMMARY")
print("-" * 70)
print(f"Materials processed: {len(material_results) if 'material_results' in locals() else 0}")
print(f"Transport routes processed: {len(transport_results) if 'transport_results' in locals() else 0}")
print()

# Show output file locations
print("Output files:")
base_dir = Path(__file__).resolve().parents[2]
print(f"  - Materials: {base_dir / 'data' / 'emissions' / 'materials_emissions.json'}")
print(f"  - Transport: {base_dir / 'data' / 'emissions' / 'transport_emissions.json'}")
print()
print("=" * 70)
