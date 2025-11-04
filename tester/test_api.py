"""
Test script for the PortOptimizer Excel Download API
This script demonstrates how to use all the API endpoints
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:5004"

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


def test_download_excel_now():
    """Test downloading an immediate Excel report"""
    print("\n" + "="*50)
    print("Testing: POST /excel/now")
    print("="*50)
    
    data = {
        "admin_password": ADMIN_PASSWORD
    }
    
    response = requests.post(
        f"{BASE_URL}/excel/now",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    return response.json().get('success', False)


def test_get_excel():
    """Test getting an Excel report by date"""
    print("\n" + "="*50)
    print("Testing: GET /excel/<date>")
    print("="*50)
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"Requesting Excel report for: {today}")
    
    response = requests.get(f"{BASE_URL}/excel/{today}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Excel report found successfully")
        print(f"Response JSON: {json.dumps(data, indent=2)}")
        
        # Verify JSON structure
        required_fields = ['success', 'date', 'filename', 'download_url', 'message']
        for field in required_fields:
            if field in data:
                print(f"✓ {field}: {data[field]}")
            else:
                print(f"❌ Missing field: {field}")
        
        # Test downloading the actual file
        if 'download_url' in data:
            download_url = data['download_url']
            print(f"\nTesting file download from: {download_url}")
            
            if download_url.startswith('http'):
                # Full URL
                file_response = requests.get(download_url)
            else:
                # Relative URL
                file_response = requests.get(f"{BASE_URL}{download_url}")
            
            if file_response.status_code == 200:
                filename = data.get('filename', 'test_excel.xlsx')
                with open(f"test_{filename}", "wb") as f:
                    f.write(file_response.content)
                print(f"✓ Excel file downloaded and saved as: test_{filename}")
            else:
                print(f"❌ Failed to download file: {file_response.status_code}")
    else:
        print(f"Response: {response.json()}")


def test_get_pdf():
    """Test getting a PDF report by date"""
    print("\n" + "="*50)
    print("Testing: GET /pdf/<date>")
    print("="*50)
    
    today = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"Requesting PDF report for: {today}")
    
    response = requests.get(f"{BASE_URL}/pdf/{today}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ PDF report found successfully")
        print(f"Response JSON: {json.dumps(data, indent=2)}")
        
        # Verify JSON structure
        required_fields = ['success', 'date', 'filename', 'download_url', 'message']
        for field in required_fields:
            if field in data:
                print(f"✓ {field}: {data[field]}")
            else:
                print(f"❌ Missing field: {field}")
        
        # Test downloading the actual file
        if 'download_url' in data:
            download_url = data['download_url']
            print(f"\nTesting file download from: {download_url}")
            
            if download_url.startswith('http'):
                # Full URL
                file_response = requests.get(download_url)
            else:
                # Relative URL
                file_response = requests.get(f"{BASE_URL}{download_url}")
            
            if file_response.status_code == 200:
                filename = data.get('filename', 'test_pdf.pdf')
                with open(f"test_{filename}", "wb") as f:
                    f.write(file_response.content)
                print(f"✓ PDF file downloaded and saved as: test_{filename}")
            else:
                print(f"❌ Failed to download file: {file_response.status_code}")
    else:
        print(f"Response: {response.json()}")


def test_get_excel_range():
    """Test getting Excel reports range"""
    print("\n" + "="*50)
    print("Testing: GET /excel/range")
    print("="*50)
    
    # Test with last_n parameter
    print("\nTesting with last_n=2")
    response = requests.get(f"{BASE_URL}/excel/range?last_n=2")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Excel reports found successfully")
        print(f"Download URL: {data.get('download_url', 'Unknown')}")
        print(f"Filename: {data.get('filename', 'Unknown')}")
    else:
        print(f"Response: {response.json()}")


def test_change_frequency():
    """Test changing Excel download frequency"""
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


def test_set_preferred_hour():
    """Test setting preferred hour for scheduled captures"""
    print("\n" + "="*50)
    print("Testing: POST /admin/preferred_hour")
    print("="*50)
    
    # Change to 2 PM (14:00)
    data = {
        "admin_password": ADMIN_PASSWORD,
        "preferred_hour": 14
    }
    
    print("Setting preferred hour to 14:00 (2 PM)")
    response = requests.post(
        f"{BASE_URL}/admin/preferred_hour",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Change back to 10 AM (10:00)
    data["preferred_hour"] = 10
    print("\nChanging back to 10:00 (10 AM)")
    response = requests.post(
        f"{BASE_URL}/admin/preferred_hour",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_update_credentials():
    """Test updating login credentials"""
    print("\n" + "="*50)
    print("Testing: POST /admin/credentials")
    print("="*50)
    
    # Update credentials
    data = {
        "admin_password": ADMIN_PASSWORD,
        "username": "test@example.com",
        "password": "testpassword123"
    }
    
    print("Updating credentials")
    response = requests.post(
        f"{BASE_URL}/admin/credentials",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Change back to original credentials
    data = {
        "admin_password": ADMIN_PASSWORD,
        "username": "sara@fouroneone.io",
        "password": "Ss925201!"
    }
    
    print("\nRestoring original credentials")
    response = requests.post(
        f"{BASE_URL}/admin/credentials",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_cleanup():
    """Test cleanup endpoint"""
    print("\n" + "="*50)
    print("Testing: POST /admin/cleanup")
    print("="*50)
    
    data = {
        "admin_password": ADMIN_PASSWORD
    }
    
    print("Running cleanup (this will delete all files)")
    response = requests.post(
        f"{BASE_URL}/admin/cleanup",
        json=data
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_download_file():
    """Test downloading a file directly"""
    print("\n" + "="*50)
    print("Testing: GET /download/<filename>")
    print("="*50)
    
    # This would need an actual filename from a previous download
    print("Note: This test requires a previously downloaded file")
    print("Run the Excel download test first to get a filename")
    
    # For demonstration, we'll just test the endpoint structure
    test_filename = "2025-01-15_12-00-00.xlsx"
    response = requests.get(f"{BASE_URL}/download/{test_filename}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"✓ File download successful")
        with open(f"downloaded_{test_filename}", "wb") as f:
            f.write(response.content)
        print(f"Saved as: downloaded_{test_filename}")
    elif response.status_code == 404:
        print(f"✓ Correctly returned 404 for non-existent file")
    else:
        print(f"Response: {response.text}")


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
    print("="*60)
    print("PortOptimizer Excel Download API - Complete Test Suite")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Make sure the API is running!")
    print("="*60)
    
    input("Press Enter to start tests...")
    
    try:
        # Basic information tests
        print("\n🔍 TESTING BASIC ENDPOINTS")
        test_root()
        test_status()
        
        # Test downloading Excel report
        print("\n📥 TESTING EXCEL DOWNLOAD")
        print("⚠️  The next test will download an Excel report (takes ~2 minutes)")
        choice = input("Do you want to test downloading an Excel report? (y/n): ")
        
        if choice.lower() == 'y':
            excel_downloaded = test_download_excel_now()
            
            if excel_downloaded:
                # Test getting reports by date
                print("\n📊 TESTING REPORT RETRIEVAL")
                test_get_excel()
                test_get_pdf()
        
        # Test file download functionality
        print("\n📁 TESTING FILE DOWNLOADS")
        test_download_file()
        
        # Test admin functions
        print("\n⚙️  TESTING ADMIN FUNCTIONS")
        test_change_frequency()
        test_set_preferred_hour()
        test_update_credentials()
        
        # Test error handling
        print("\n❌ TESTING ERROR HANDLING")
        test_invalid_admin_password()
        
        # Optional cleanup test
        print("\n🧹 OPTIONAL CLEANUP TEST")
        cleanup_choice = input("Do you want to test cleanup (deletes all files)? (y/n): ")
        if cleanup_choice.lower() == 'y':
            test_cleanup()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED!")
        print("="*60)
        print("Summary of tested endpoints:")
        print("• GET  /                    - API information")
        print("• GET  /status              - System status")
        print("• POST /excel/now           - Download Excel + convert to PDF")
        print("• GET  /excel/<date>        - Get Excel report by date")
        print("• GET  /pdf/<date>          - Get PDF report by date")
        print("• GET  /download/<filename> - Download specific file")
        print("• POST /admin/frequency     - Change frequency")
        print("• POST /admin/preferred_hour - Set preferred hour")
        print("• POST /admin/credentials   - Update credentials")
        print("• POST /admin/cleanup       - Delete all files")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API")
        print("Make sure the Flask app is running on http://localhost:5004")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()

