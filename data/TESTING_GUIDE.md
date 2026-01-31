# Testing the Emissions Calculation System

## Quick Start - Run All Tests

Open PowerShell in the project directory and run:

```powershell
cd c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\calculate_emission
$env:PYTHONPATH="c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\src"
python test_emissions_system.py
```

This will run both material and transport emissions calculations and show you the results.

---

## Individual Component Testing

### 1. Test Material Emissions Only

```powershell
cd c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\calculate_emission
$env:PYTHONPATH="c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\src"
python calc_material_emissions.py
```

**What it does:**
- Loads material data from `data/raw/sample_materials.csv`
- Filters for Steel, Recycled Steel, and Aluminum only
- Calculates emissions using ClimateQ API
- Saves results to `data/emissions/materials_emissions.json`

**Expected output:**
```
============================================================
MATERIAL EMISSIONS CALCULATION
============================================================
[LOAD] Loading sample_materials.csv...
[OK] Loaded 8 records from 1 file(s)
[INFO] Filtering for allowed materials: Steel, Recycled Steel, Aluminum
[OK] Company A - Steel (500.00 kg) -> 820.00 kg CO2e
[OK] Company B - Recycled Steel (300.00 kg) -> 219.00 kg CO2e
...
[SKIP] Material 'Copper' not in allowed list, skipping...
```

---

### 2. Test Transport Emissions Only

```powershell
cd c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\calculate_emission
$env:PYTHONPATH="c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\src"
python calc_transport_emissions.py
```

**What it does:**
- Loads transport data from `data/raw/sample_transport.csv` and `data/raw/transport_intermodal_test.csv`
- Filters for rail, ship, air, and intermodal modes only
- Calculates emissions using ClimateQ API
- Handles intermodal routes with multi-leg calculations
- Saves results to `data/emissions/transport_emissions.json`

**Expected output:**
```
============================================================
TRANSPORT EMISSIONS CALCULATION
============================================================
[LOAD] Loading sample_transport.csv...
[LOAD] Loading transport_intermodal_test.csv...
[OK] Loaded 13 records from 2 file(s)
[INFO] Filtering for allowed transport modes: rail, ship, air, intermodal
[INFO] Intermodal distance estimation enabled
[SKIP] Transport mode 'truck' not in allowed list, skipping...
[OK] Company C - Aluminum via ship (289.07 t*km) -> 5.86 kg CO2e
  [LEG] rail (1287.47 km, 40%) -> 17.85 kg CO2e
  [LEG] ship (1287.47 km, 40%) -> 13.03 kg CO2e
  [LEG] air (643.74 km, 20%) -> 549.11 kg CO2e
[OK] Company A - Steel via intermodal (3218.68 km) -> 579.99 kg CO2e
```

---

### 3. Test Data Loader

```powershell
cd c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\src
python universal_data_loader.py
```

**What it does:**
- Tests the universal data loader
- Loads all data sources (materials, transport, energy)
- Shows summary of loaded data

---

### 4. Verify Output Files

After running the tests, check the output files:

**Materials Emissions:**
```powershell
cat c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\emissions\materials_emissions.json
```

**Transport Emissions:**
```powershell
cat c:\Users\punit\HACKCELERATE-Project-Stardust-Crusaders\data\emissions\transport_emissions.json
```

---

## What to Look For

### ✅ Success Indicators

1. **No API errors** - All ClimateQ API calls should return 200 status
2. **Filtering works** - Copper and Truck should be skipped
3. **Intermodal calculations** - Should show multiple legs with emissions breakdown
4. **Output files created** - JSON files should exist in `data/emissions/`
5. **Reasonable emissions values** - Numbers should be positive and logical

### ❌ Common Issues

**Issue:** `ModuleNotFoundError: No module named 'universal_data_loader'`
- **Fix:** Make sure to set `$env:PYTHONPATH` before running

**Issue:** API errors or "no emission factors found"
- **Fix:** Check that `data_config.json` has the correct activity IDs

**Issue:** No data loaded
- **Fix:** Verify CSV files exist in `data/raw/` directory

---

## Sample Data Files

The system uses these sample data files:

- `data/raw/sample_materials.csv` - Material usage data
- `data/raw/sample_transport.csv` - Transport routes (includes trucks to test filtering)
- `data/raw/transport_intermodal_test.csv` - Intermodal transport routes

You can add more CSV files following the same format, and they'll be automatically loaded.
