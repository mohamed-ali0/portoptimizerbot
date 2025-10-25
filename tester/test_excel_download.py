"""
Test script for Excel download functionality
"""
import requests
import json
from datetime import datetime

def test_excel_download():
    """Test the Excel download functionality"""
    base_url = "http://localhost:5000"
    
    print("="*60)
    print("TESTING EXCEL DOWNLOAD FUNCTIONALITY")
    print("="*60)
    print()
    
    # Test 1: Download Excel report immediately
    print("1. Testing immediate Excel download...")
    try:
        response = requests.post(f"{base_url}/excel/now", 
                               json={"admin_password": "admin123"})
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('message', 'Unknown')}")
            print(f"   Filename: {data.get('filename', 'Unknown')}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print()
    
    # Test 2: Get Excel report for today
    print("2. Testing get Excel report for today...")
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        response = requests.get(f"{base_url}/excel/{today}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('message', 'Unknown')}")
            print(f"   Download URL: {data.get('download_url', 'Unknown')}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print()
    
    # Test 3: Check system status
    print("3. Testing system status...")
    try:
        response = requests.get(f"{base_url}/status")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success: {data.get('message', 'Unknown')}")
            print(f"   Last Excel: {data.get('last_screenshot', 'Unknown')}")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    print()
    print("="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    test_excel_download()
