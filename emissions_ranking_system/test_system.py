import requests
import json
import subprocess
import time
import os

def test_ranking_system():
    """Test the ranking system functionality."""
    print("Testing Emissions Ranking System...")

    # Test standalone ranking
    print("\n1. Testing standalone ranking system...")
    result = subprocess.run(['python', 'ranking_system.py'], capture_output=True, text=True, cwd=os.getcwd())
    if result.returncode == 0:
        print("✓ Standalone ranking system works")
        print("Output:", result.stdout[-500:])  # Last 500 chars
    else:
        print("✗ Standalone ranking system failed")
        print("Error:", result.stderr)

    # Test API server (start in background)
    print("\n2. Testing API server...")
    server_process = subprocess.Popen(['python', 'api_server.py'], cwd=os.getcwd())

    # Wait for server to start
    time.sleep(3)

    try:
        # Test materials endpoint
        response = requests.get('http://localhost:5000/api/rankings/materials')
        if response.status_code == 200:
            data = response.json()
            print("✓ Materials API endpoint works")
            print(f"   Returned {len(data['data'])} materials")
        else:
            print("✗ Materials API endpoint failed")

        # Test transport endpoint
        response = requests.get('http://localhost:5000/api/rankings/transport')
        if response.status_code == 200:
            data = response.json()
            print("✓ Transport API endpoint works")
            print(f"   Returned {len(data['data'])} transport modes")
        else:
            print("✗ Transport API endpoint failed")

        # Test all rankings endpoint
        response = requests.get('http://localhost:5000/api/rankings/all')
        if response.status_code == 200:
            data = response.json()
            print("✓ All rankings API endpoint works")
            print(f"   Materials: {len(data['materials'])}, Transport: {len(data['transport'])}")
        else:
            print("✗ All rankings API endpoint failed")

        # Test update endpoint
        response = requests.post('http://localhost:5000/api/rankings/update')
        if response.status_code == 200:
            print("✓ Update API endpoint works")
        else:
            print("✗ Update API endpoint failed")

    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to API server")
    finally:
        server_process.terminate()
        server_process.wait()

    # Check if files were created
    print("\n3. Checking file creation...")
    files_to_check = ['current_rankings.json', 'ranking_audit.log']
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✓ {file} created")
        else:
            print(f"✗ {file} not found")

    print("\nTesting completed!")

if __name__ == "__main__":
    test_ranking_system()
