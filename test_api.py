"""
Test script for the PortOptimizer Screenshot API
This script demonstrates how to use all the API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://37.60.243.201:5004"

# Admin password
ADMIN_PASSWORD = "YB02Ss3JJdk"


def test_root():
    """Test the root endpoint"""
    print("\n" + "="*50)
    print("Testing: GET /")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_status():
    """Test the status endpoint"""
    print("\n" + "="*50)
    print("Testing: GET /status")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/status")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_take_screenshot_now():
    """Test taking an immediate screenshot"""
    print("\n" + "="*50)
    print("Testing: POST /screenshot/now")
    print("="*50)
    
    data = {
        "admin_password": ADMIN_PASSWORD
    }
    
    response = requests.post(
        f"{BASE_URL}/screenshot/now",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json().get('success', False)


def test_get_screenshot():
    """Test getting a screenshot by date"""
    print("\n" + "="*50)
    print("Testing: GET /screenshot/<date>")
    print("="*50)
    
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Requesting screenshot for: {today}")
    
    response = requests.get(f"{BASE_URL}/screenshot/{today}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✓ Screenshot downloaded successfully")
        # Save to file
        with open(f"test_screenshot_{today}.png", "wb") as f:
            f.write(response.content)
        print(f"Saved to: test_screenshot_{today}.png")
    else:
        print(f"Response: {response.json()}")


def test_get_screenshots_range():
    """Test getting screenshots range"""
    print("\n" + "="*50)
    print("Testing: GET /screenshots/range")
    print("="*50)
    
    # Test with last_n parameter
    print("\nTesting with last_n=2")
    response = requests.get(f"{BASE_URL}/screenshots/range?last_n=2")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✓ ZIP file downloaded successfully")
        with open("test_screenshots_last_2.zip", "wb") as f:
            f.write(response.content)
        print(f"Saved to: test_screenshots_last_2.zip")
    else:
        print(f"Response: {response.json()}")


def test_change_frequency():
    """Test changing screenshot frequency"""
    print("\n" + "="*50)
    print("Testing: POST /admin/frequency")
    print("="*50)
    
    # Change to 12 hours
    data = {
        "admin_password": ADMIN_PASSWORD,
        "frequency_hours": 12
    }
    
    print("Setting frequency to 12 hours")
    response = requests.post(
        f"{BASE_URL}/admin/frequency",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Change back to 24 hours
    data["frequency_hours"] = 24
    print("\nChanging back to 24 hours")
    response = requests.post(
        f"{BASE_URL}/admin/frequency",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_invalid_admin_password():
    """Test with invalid admin password"""
    print("\n" + "="*50)
    print("Testing: Invalid Admin Password")
    print("="*50)
    
    data = {
        "admin_password": "wrong_password",
        "frequency_hours": 12
    }
    
    response = requests.post(
        f"{BASE_URL}/admin/frequency",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 403:
        print("✓ Correctly rejected invalid password")


def main():
    """Run all tests"""
    print("="*50)
    print("PortOptimizer Screenshot API - Test Suite")
    print("="*50)
    print(f"Base URL: {BASE_URL}")
    print(f"Make sure the API is running!")
    print("="*50)
    
    input("Press Enter to start tests...")
    
    try:
        # Basic tests
        test_root()
        test_status()
        
        # Test taking screenshot
        print("\n⚠️  The next test will take a screenshot (takes ~2 minutes)")
        choice = input("Do you want to test taking a screenshot? (y/n): ")
        
        if choice.lower() == 'y':
            screenshot_taken = test_take_screenshot_now()
            
            if screenshot_taken:
                # Test getting the screenshot
                test_get_screenshot()
                test_get_screenshots_range()
        
        # Test admin functions
        test_change_frequency()
        test_invalid_admin_password()
        
        print("\n" + "="*50)
        print("✓ All tests completed!")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API")
        print("Make sure the Flask app is running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()

