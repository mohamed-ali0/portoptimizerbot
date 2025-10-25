"""
Simple Excel to PDF conversion - Legal Landscape
Just converts Excel to PDF without borders
"""
import os
import subprocess
import time
from datetime import datetime

def find_latest_excel():
    """Find the most recent Excel file"""
    screenshots_dir = "screenshots"
    
    if not os.path.exists(screenshots_dir):
        return None
    
    excel_files = []
    for file in os.listdir(screenshots_dir):
        if file.endswith(('.xlsx', '.xls')):
            excel_files.append(os.path.join(screenshots_dir, file))
    
    if not excel_files:
        return None
    
    return max(excel_files, key=os.path.getctime)

def convert_to_pdf_simple(excel_path, pdf_path):
    """
    Simple Excel to PDF conversion - Legal Landscape
    """
    try:
        print(f"Converting Excel to PDF...")
        print(f"Input: {excel_path}")
        print(f"Output: {pdf_path}")
        
        # Method 1: Try using win32com (Excel automation)
        try:
            import win32com.client
            
            print("Using Excel automation...")
            
            # Start Excel
            excel = win32com.client.Dispatch("Excel.Application")
            excel.Visible = False
            excel.DisplayAlerts = False
            
            # Open the Excel file
            workbook = excel.Workbooks.Open(os.path.abspath(excel_path))
            worksheet = workbook.ActiveSheet
            
            # Set page orientation to landscape
            worksheet.PageSetup.Orientation = 2  # xlLandscape
            worksheet.PageSetup.PaperSize = 5    # xlPaperLegal
            
            # Export as PDF
            workbook.ExportAsFixedFormat(
                Type=0,  # xlTypePDF
                Filename=os.path.abspath(pdf_path),
                Quality=0,  # xlQualityStandard
                IncludeDocProps=True,
                IgnorePrintAreas=False,
                From=1,
                To=1,
                OpenAfterPublish=False
            )
            
            # Close Excel
            workbook.Close()
            excel.Quit()
            
            print(f"✅ PDF created using Excel: {pdf_path}")
            return True
            
        except ImportError:
            print("win32com not available")
        except Exception as e:
            print(f"Excel automation failed: {str(e)}")
        
        # Method 2: Try using LibreOffice
        try:
            print("Trying LibreOffice...")
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', os.path.dirname(pdf_path),
                '--infilter=calc8',
                excel_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                # LibreOffice creates PDF with same name as Excel file
                expected_pdf = excel_path.replace('.xlsx', '.pdf')
                if os.path.exists(expected_pdf):
                    # Move to desired location
                    os.rename(expected_pdf, pdf_path)
                    print(f"✅ PDF created using LibreOffice: {pdf_path}")
                    return True
            else:
                print(f"LibreOffice failed: {result.stderr}")
        except Exception as e:
            print(f"LibreOffice not available: {str(e)}")
        
        # Method 3: Try using PowerShell
        try:
            print("Trying PowerShell...")
            ps_script = f"""
            $excel = New-Object -ComObject Excel.Application
            $excel.Visible = $false
            $excel.DisplayAlerts = $false
            
            $workbook = $excel.Workbooks.Open('{os.path.abspath(excel_path)}')
            $worksheet = $workbook.ActiveSheet
            
            $worksheet.PageSetup.Orientation = 2
            $worksheet.PageSetup.PaperSize = 5
            
            $workbook.ExportAsFixedFormat(0, '{os.path.abspath(pdf_path)}')
            
            $workbook.Close()
            $excel.Quit()
            [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel)
            """
            
            # Save PowerShell script
            with open("temp_convert.ps1", "w") as f:
                f.write(ps_script)
            
            # Run PowerShell script
            result = subprocess.run([
                "powershell", "-ExecutionPolicy", "Bypass", "-File", "temp_convert.ps1"
            ], capture_output=True, text=True, timeout=60)
            
            # Clean up
            os.remove("temp_convert.ps1")
            
            if result.returncode == 0:
                print(f"✅ PDF created using PowerShell: {pdf_path}")
                return True
            else:
                print(f"PowerShell failed: {result.stderr}")
                
        except Exception as e:
            print(f"PowerShell method failed: {str(e)}")
        
        print("❌ All conversion methods failed")
        return False
        
    except Exception as e:
        print(f"❌ Error in PDF conversion: {str(e)}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("SIMPLE EXCEL TO PDF CONVERSION")
    print("="*60)
    print("Converts Excel to Legal Landscape PDF")
    print("="*60)
    
    # Find latest Excel file
    excel_path = find_latest_excel()
    if not excel_path:
        print("❌ No Excel files found in screenshots directory")
        return
    
    print(f"📁 Found Excel file: {excel_path}")
    
    # Create PDF path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path = f"screenshots/simple_pdf_{timestamp}.pdf"
    
    # Convert to PDF
    if convert_to_pdf_simple(excel_path, pdf_path):
        print(f"\n🎯 SUCCESS!")
        print(f"✅ PDF created: {pdf_path}")
        print("\nThe PDF is now ready in legal landscape format!")
    else:
        print("\n❌ PDF conversion failed")
        print("Try opening the Excel file manually and pressing Ctrl+P")

if __name__ == "__main__":
    main()