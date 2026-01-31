from flask import Flask, jsonify, request, send_from_directory
from ranking_system import EmissionsRankingSystem
import logging
import os
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for development
CORS(app)

# Initialize ranking system (loads data from files)
ranking_system = EmissionsRankingSystem()

@app.route('/')
def serve_frontend():
    return send_from_directory('static', 'index.html')

# Set up logging
logging.basicConfig(level=logging.INFO)

@app.route('/api/rankings/materials', methods=['GET'])
def get_materials_ranking():
    """API endpoint to get materials ranking."""
    try:
        ranking = ranking_system.get_materials_ranking()
        return jsonify({
            'status': 'success',
            'data': [{'rank': i+1, 'material': item[0], 'emissions': item[1]} for i, item in enumerate(ranking)],
            'last_update': ranking_system.last_update.isoformat() if ranking_system.last_update else None
        })
    except Exception as e:
        logging.error(f"Error fetching materials ranking: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/rankings/transport', methods=['GET'])
def get_transport_ranking():
    """API endpoint to get transport ranking."""
    try:
        ranking = ranking_system.get_transport_ranking()
        return jsonify({
            'status': 'success',
            'data': [{'rank': i+1, 'mode': item[0], 'emissions': item[1]} for i, item in enumerate(ranking)],
            'last_update': ranking_system.last_update.isoformat() if ranking_system.last_update else None
        })
    except Exception as e:
        logging.error(f"Error fetching transport ranking: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/rankings/all', methods=['GET'])
def get_all_rankings():
    """API endpoint to get both materials and transport rankings."""
    try:
        # Ensure we have data loaded
        if not ranking_system.materials_ranking:
             ranking_system.update_rankings()
             
        materials = ranking_system.get_materials_ranking()
        transport = ranking_system.get_transport_ranking()
        
        print(f"[DEBUG] API Request: returning {len(materials)} materials and {len(transport)} transport records")
        
        return jsonify({
            'status': 'success',
            'materials': [{'rank': i+1, 'material': item[0], 'emissions': item[1]} for i, item in enumerate(materials)],
            'transport': [{'rank': i+1, 'mode': item[0], 'emissions': item[1]} for i, item in enumerate(transport)],
            'last_update': ranking_system.last_update.isoformat() if ranking_system.last_update else None
        })
    except Exception as e:
        logging.error(f"Error fetching all rankings: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Endpoint to MANUALLY trigger update if needed
@app.route('/api/rankings/refresh', methods=['POST'])
def manual_update():
    try:
        ranking_system.update_rankings()
        ranking_system.save_rankings_to_file()
        return jsonify({'status': 'success', 'message': 'Rankings refreshed from CSVs'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Simple Ranking Server Started")
    print("Dashboard available at: http://localhost:5000")
    print("NOTE: Auto-updates disabled. Data is loaded from existing CSVs/JSON.")
    print("="*50 + "\n")
    
    # Try to load existing rankings on startup
    try:
        ranking_system.update_rankings()
    except Exception as e:
        print(f"Warning: Could not load initial rankings: {e}")

    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

