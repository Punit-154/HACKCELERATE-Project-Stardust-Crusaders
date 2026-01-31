# Dynamic Emissions Ranking System

This system provides independent tracking and ranking of materials and transport by CO₂e emissions, designed for real-time updates and backend readiness for frontend integration. It processes raw CSV data using calculation scripts and generates live rankings.

## Features

- **Independent Ranking**: Separate rankings for materials and transport modes by total CO₂e emissions.
- **Descending Order**: Rankings sorted from highest to lowest emissions.
- **Dynamic Updates**: Automatic updates when new data is ingested.
- **Real-time Reflection**: Immediate updates to rankings upon data changes.
- **Consistency**: Ensures accurate and consistent emission calculations.
- **Auditability**: Comprehensive logging of all ranking updates.
- **Backend API**: RESTful API endpoints for frontend integration.
- **Raw Data Processing**: Loads and processes CSV data using dedicated calculation scripts.

## Requirements

- Python 3.7+
- Flask
- Pandas
- Raw data files: `sample_materials.csv` and `sample_transport.csv`

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure the following files are in the same directory:
   - `sample_materials.csv` - Raw materials data
   - `sample_transport.csv` - Raw transport data

## Usage

### Standalone Ranking

Run the ranking system directly:
```bash
python ranking_system.py
```

This will:
1. Load data from `sample_materials.csv` and `sample_transport.csv`
2. Calculate emissions using built-in calculation logic
3. Generate rankings for materials and transport
4. Save rankings to `current_rankings.json`
5. Display rankings in the console

### API Server

Start the Flask API server:
```bash
python api_server.py
```

The server will run on `http://localhost:5000` with the following endpoints:

#### Rankings Endpoints
- `GET /api/rankings/materials`: Get materials ranking
- `GET /api/rankings/transport`: Get transport ranking
- `GET /api/rankings/all`: Get both rankings
- `POST /api/rankings/update`: Trigger manual ranking update

#### Data Endpoints
- `GET /api/data/materials`: Get raw materials data from CSV
- `GET /api/data/transport`: Get raw transport data from CSV

### API Response Format

```json
{
  "status": "success",
  "data": [
    {
      "rank": 1,
      "material": "Aluminum",
      "emissions": 12345.67
    }
  ],
  "last_update": "2023-10-01T12:00:00"
}
```

## System Architecture

- `ranking_system.py`: Core ranking logic, data loading, and emission calculations
- `api_server.py`: Flask API server with endpoints for rankings and raw data
- `calc_material_emissions.py`: Material emissions calculation script (reference)
- `calc_transport_emissions.py`: Transport emissions calculation script (reference)
- `sample_materials.csv`: Raw materials data input
- `sample_transport.csv`: Raw transport data input
- `current_rankings.json`: Persistent rankings storage
- `ranking_audit.log`: Audit log for all updates

## Data Flow

1. Load raw CSV data from `sample_materials.csv` and `sample_transport.csv`
2. Calculate emissions for each material and transport entry using built-in logic
3. Aggregate emissions by material type and transport mode
4. Sort by emissions in descending order to create rankings
5. Save rankings and log updates
6. Serve rankings and raw data via API endpoints

## Calculation Logic

### Materials Emissions
- Steel: 1.85 kg CO₂e per kg
- Aluminum: 8.24 kg CO₂e per kg
- Recycled Steel: 0.73 kg CO₂e per kg
- Cement: 0.85 kg CO₂e per kg
- Iron Wire: 1.95 kg CO₂e per kg

### Transport Emissions
- Truck: 0.0001 kg CO₂e per tonne-km
- Ship: 0.00002 kg CO₂e per tonne-km
- Rail: 0.000015 kg CO₂e per tonne-km
- Air: 0.0005 kg CO₂e per tonne-km

## Integration

This backend system is ready for frontend integration. Use the API endpoints to fetch rankings and raw data, and implement real-time updates in your frontend application. The system automatically updates rankings every hour and provides audit logging for all changes.
