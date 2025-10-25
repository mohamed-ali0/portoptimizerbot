"""
Quick Excel to PDF conversion
Just converts Excel to Legal Landscape PDF
"""
import os
import subprocess
from datetime import datetime

def main():
    print("="*50)
    print("QUICK EXCEL TO PDF CONVERSION")
    print("="*50)
    
    # Find latest Excel file
    screenshots_dir = "screenshots"
    excel_files = []
    
    if os.path.exists(screenshots_dir):
        for file in os.listdir(screenshots_dir):
            if file.endswith(('.xlsx', '.xls')) and not file.startswith('~$'):
                excel_files.append(os.path.join(screenshots_dir, file))
    
    if not excel_files:
        print("❌ No Excel files found")
        return
    
    # Get most recent file
    latest_excel = max(excel_files, key=os.path.getctime)
    print(f"📁 Found: {latest_excel}")
    
    # Create PDF path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path = f"screenshots/quick_pdf_{timestamp}.pdf"
    
    # Try simple conversion methods
    print("Converting to PDF...")
    
    # Method 1: Try LibreOffice
    try:
        cmd = ['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', 'screenshots', latest_excel]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Find the created PDF
            expected_pdf = latest_excel.replace('.xlsx', '.pdf')
            if os.path.exists(expected_pdf):
                os.rename(expected_pdf, pdf_path)
                print(f"✅ PDF created: {pdf_path}")
                return
    except:
        pass
    
    # Method 2: Try PowerShell
    try:
        ps_script = f"""
        $excel = New-Object -ComObject Excel.Application
        $excel.Visible = $false
        $excel.DisplayAlerts = $false
        $workbook = $excel.Workbooks.Open('{os.path.abspath(latest_excel)}')
        $worksheet = $workbook.ActiveSheet
        $worksheet.PageSetup.Orientation = 2
        $worksheet.PageSetup.PaperSize = 5
        $workbook.ExportAsFixedFormat(0, '{os.path.abspath(pdf_path)}')
        $workbook.Close()
        $excel.Quit()
        """
        
        with open("temp.ps1", "w") as f:
            f.write(ps_script)
        
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "temp.ps1"], timeout=60)
        os.remove("temp.ps1")
        
        if os.path.exists(pdf_path):
            print(f"✅ PDF created: {pdf_path}")
            return
    except:
        pass
    
    print("❌ Conversion failed")
    print("Try opening Excel manually and pressing Ctrl+P")

if __name__ == "__main__":
    main()
