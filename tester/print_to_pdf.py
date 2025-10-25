"""
Simple print to PDF using Windows print functionality
This mimics exactly what you do in Excel: add borders and print to PDF
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
    
    # Get the most recent file
    latest_file = max(excel_files, key=os.path.getctime)
    return latest_file

def print_to_pdf_windows(excel_path, pdf_path):
    """
    Use Windows print to PDF functionality
    This is the most reliable method - like pressing Ctrl+P in Excel
    """
    try:
        print(f"Using Windows print to PDF...")
        print(f"Excel file: {excel_path}")
        print(f"PDF output: {pdf_path}")
        
        # Method 1: Use Windows print to PDF via PowerShell
        try:
            # Create PowerShell script to print to PDF
            ps_script = f"""
            $excel = New-Object -ComObject Excel.Application
            $excel.Visible = $false
            $excel.DisplayAlerts = $false
            
            $workbook = $excel.Workbooks.Open('{os.path.abspath(excel_path)}')
            $worksheet = $workbook.ActiveSheet
            
            # Set page orientation to landscape
            $worksheet.PageSetup.Orientation = 2  # xlLandscape
            $worksheet.PageSetup.PaperSize = 5   # xlPaperLegal
            
            # Export as PDF
            $workbook.ExportAsFixedFormat(0, '{os.path.abspath(pdf_path)}')
            
            $workbook.Close()
            $excel.Quit()
            [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel)
            """
            
            # Save PowerShell script
            with open("temp_print.ps1", "w") as f:
                f.write(ps_script)
            
            # Run PowerShell script
            result = subprocess.run([
                "powershell", "-ExecutionPolicy", "Bypass", "-File", "temp_print.ps1"
            ], capture_output=True, text=True, timeout=60)
            
            # Clean up
            os.remove("temp_print.ps1")
            
            if result.returncode == 0:
                print(f"✅ PDF created using Windows print: {pdf_path}")
                return True
            else:
                print(f"PowerShell failed: {result.stderr}")
                
        except Exception as e:
            print(f"PowerShell method failed: {str(e)}")
        
        # Method 2: Use VBScript (alternative)
        try:
            print("Trying VBScript method...")
            
            vbs_script = f"""
            Set objExcel = CreateObject("Excel.Application")
            objExcel.Visible = False
            objExcel.DisplayAlerts = False
            
            Set objWorkbook = objExcel.Workbooks.Open("{os.path.abspath(excel_path)}")
            Set objWorksheet = objWorkbook.ActiveSheet
            
            objWorksheet.PageSetup.Orientation = 2
            objWorksheet.PageSetup.PaperSize = 5
            
            objWorkbook.ExportAsFixedFormat 0, "{os.path.abspath(pdf_path)}"
            
            objWorkbook.Close
            objExcel.Quit
            """
            
            # Save VBScript
            with open("temp_print.vbs", "w") as f:
                f.write(vbs_script)
            
            # Run VBScript
            result = subprocess.run([
                "cscript", "//nologo", "temp_print.vbs"
            ], capture_output=True, text=True, timeout=60)
            
            # Clean up
            os.remove("temp_print.vbs")
            
            if result.returncode == 0:
                print(f"✅ PDF created using VBScript: {pdf_path}")
                return True
            else:
                print(f"VBScript failed: {result.stderr}")
                
        except Exception as e:
            print(f"VBScript method failed: {str(e)}")
        
        print("❌ All Windows print methods failed")
        return False
        
    except Exception as e:
        print(f"❌ Error in Windows print: {str(e)}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("WINDOWS PRINT TO PDF")
    print("="*60)
    print("This uses Windows built-in print to PDF functionality")
    print("Like pressing Ctrl+P in Excel and selecting 'Microsoft Print to PDF'")
    print("="*60)
    
    # Find the latest Excel file
    excel_path = find_latest_excel()
    if not excel_path:
        print("❌ No Excel files found in screenshots directory")
        return
    
    print(f"📁 Found Excel file: {excel_path}")
    
    # Create PDF path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path = f"screenshots/windows_print_{timestamp}.pdf"
    
    # Convert to PDF
    if print_to_pdf_windows(excel_path, pdf_path):
        print(f"\n🎯 SUCCESS!")
        print(f"✅ PDF created: {pdf_path}")
        print("\nThis PDF should have proper formatting and borders!")
    else:
        print("\n❌ PDF conversion failed")
        print("Try opening the Excel file manually and pressing Ctrl+P")

if __name__ == "__main__":
    main()
