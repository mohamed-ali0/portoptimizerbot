import os
import pandas as pd
from reportlab.lib.pagesizes import legal, landscape
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib import colors
from datetime import datetime

def test_simple_pdf_conversion():
    """Test simple Excel to PDF conversion - legal landscape, no modifications"""
    print("=" * 60)
    print("TESTING SIMPLE PDF CONVERSION - LEGAL LANDSCAPE")
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
    pdf_path = os.path.join(test_output_dir, f"{excel_name}_simple.pdf")
    
    print(f"Input: {excel_path}")
    print(f"Output: {pdf_path}")
    
    try:
        print("\nReading Excel file...")
        # Read Excel file
        df = pd.read_excel(excel_path, sheet_name=0)
        print(f"SUCCESS: Read {len(df)} rows, {len(df.columns)} columns")
        
        print("\nCreating PDF in Legal Landscape format...")
        # Create PDF with Legal landscape page size
        doc = SimpleDocTemplate(pdf_path, pagesize=landscape(legal))
        
        # Convert DataFrame to table data - NO STYLING, NO BORDERS, NO MODIFICATIONS
        table_data = [df.columns.tolist()] + df.values.tolist()
        
        print(f"Table data: {len(table_data)} rows")
        
        # Create table - NO STYLING
        table = Table(table_data)
        
        # NO table style - just plain conversion
        print("Building PDF...")
        # Build PDF
        doc.build([table])
        
        # Check if PDF was created
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"\nSUCCESS: PDF created successfully!")
            print(f"File: {pdf_path}")
            print(f"Size: {file_size} bytes")
            print("Format: Legal Landscape (no borders, no styling)")
            return True
        else:
            print("ERROR: PDF file not found after creation")
            return False
            
    except Exception as e:
        print(f"ERROR: Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_pdf_conversion()
    
    if success:
        print("\n" + "=" * 60)
        print("SUCCESS: Simple PDF conversion works!")
        print("This is just Excel -> PDF in Legal Landscape format")
        print("No borders, no styling, no modifications")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("FAILURE: Simple PDF conversion failed")
        print("Check the error messages above.")
        print("=" * 60)
