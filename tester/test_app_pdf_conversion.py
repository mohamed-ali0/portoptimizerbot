import os
import sys
from datetime import datetime

# Add the current directory to Python path so we can import from app.py
sys.path.append('.')

# Import the conversion function from app.py
from app import convert_excel_to_pdf

def test_app_pdf_conversion():
    """Test the PDF conversion function from app.py"""
    print("=" * 60)
    print("TESTING APP.PY PDF CONVERSION")
    print("=" * 60)
    
    # Find Excel file
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        print("ERROR: Downloads directory not found")
        return False
    
    excel_files = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith(('.xlsx', '.xls')) and not filename.startswith('~$'):
            excel_files.append(filename)
    
    if not excel_files:
        print("ERROR: No Excel files found")
        return False
    
    # Get the most recent file
    latest_file = max(excel_files, key=lambda x: os.path.getctime(os.path.join(downloads_dir, x)))
    excel_path = os.path.join(downloads_dir, latest_file)
    
    print(f"SUCCESS: Found Excel file: {latest_file}")
    
    # Create test output directory
    test_output_dir = "test_pdf_output"
    os.makedirs(test_output_dir, exist_ok=True)
    
    # Expected output path
    excel_name = os.path.splitext(os.path.basename(excel_path))[0]
    pdf_path = os.path.join(test_output_dir, f"{excel_name}_app_test.pdf")
    
    print(f"Input: {excel_path}")
    print(f"Output: {pdf_path}")
    
    print("\nTesting app.py convert_excel_to_pdf function...")
    
    # Test the function from app.py
    success = convert_excel_to_pdf(excel_path, pdf_path)
    
    if success and os.path.exists(pdf_path):
        file_size = os.path.getsize(pdf_path)
        print(f"\nSUCCESS: PDF created successfully!")
        print(f"File: {pdf_path}")
        print(f"Size: {file_size} bytes")
        return True
    else:
        print(f"\nFAILURE: PDF conversion failed")
        return False

if __name__ == "__main__":
    success = test_app_pdf_conversion()
    
    if success:
        print("\n" + "=" * 60)
        print("SUCCESS: App.py PDF conversion works!")
        print("The fallback method is working correctly.")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("FAILURE: App.py PDF conversion failed")
        print("Check the error messages above.")
        print("=" * 60)
