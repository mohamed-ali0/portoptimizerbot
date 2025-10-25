"""
List Excel files and convert to PDF
"""
import os
import subprocess
from datetime import datetime

def list_excel_files():
    """List all Excel files in screenshots directory"""
    screenshots_dir = "screenshots"
    
    if not os.path.exists(screenshots_dir):
        print("❌ Screenshots directory not found")
        return []
    
    excel_files = []
    for file in os.listdir(screenshots_dir):
        if file.endswith(('.xlsx', '.xls')) and not file.startswith('~$'):
            file_path = os.path.join(screenshots_dir, file)
            file_size = os.path.getsize(file_path)
            excel_files.append((file_path, file, file_size))
    
    return excel_files

def convert_to_pdf(excel_path, pdf_path):
    """Convert Excel to PDF using LibreOffice"""
    try:
        print(f"Converting {excel_path} to PDF...")
        
        # Use LibreOffice
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', 'screenshots',
            excel_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Find the created PDF
            expected_pdf = excel_path.replace('.xlsx', '.pdf')
            if os.path.exists(expected_pdf):
                # Rename to desired name
                os.rename(expected_pdf, pdf_path)
                print(f"✅ PDF created: {pdf_path}")
                return True
            else:
                print("❌ PDF file not found after conversion")
                return False
        else:
            print(f"❌ LibreOffice failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Conversion failed: {str(e)}")
        return False

def main():
    print("="*60)
    print("EXCEL TO PDF CONVERTER")
    print("="*60)
    
    # List all Excel files
    excel_files = list_excel_files()
    
    if not excel_files:
        print("❌ No Excel files found in screenshots directory")
        return
    
    print(f"Found {len(excel_files)} Excel file(s):")
    print("-" * 60)
    
    for i, (file_path, filename, file_size) in enumerate(excel_files, 1):
        print(f"{i}. {filename} ({file_size:,} bytes)")
    
    print("-" * 60)
    
    # Let user choose
    try:
        choice = int(input("Enter the number of the file to convert (or 0 to exit): "))
        
        if choice == 0:
            print("Exiting...")
            return
        
        if 1 <= choice <= len(excel_files):
            selected_file = excel_files[choice - 1][0]
            print(f"\nSelected: {selected_file}")
            
            # Create PDF path
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            pdf_path = f"screenshots/converted_{timestamp}.pdf"
            
            # Convert to PDF
            if convert_to_pdf(selected_file, pdf_path):
                print(f"\n🎯 SUCCESS!")
                print(f"✅ PDF created: {pdf_path}")
                print("\nThe PDF is ready!")
            else:
                print("\n❌ Conversion failed")
        else:
            print("❌ Invalid choice")
            
    except ValueError:
        print("❌ Please enter a valid number")
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
