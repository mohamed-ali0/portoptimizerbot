"""
Convert the latest Excel file to PDF
"""
import os
import subprocess
from datetime import datetime

def main():
    print("="*50)
    print("CONVERT LATEST EXCEL TO PDF")
    print("="*50)
    
    # Find latest Excel file (skip temporary files)
    screenshots_dir = "screenshots"
    
    if not os.path.exists(screenshots_dir):
        print("❌ Screenshots directory not found")
        return
    
    excel_files = []
    for file in os.listdir(screenshots_dir):
        if file.endswith(('.xlsx', '.xls')) and not file.startswith('~$'):
            file_path = os.path.join(screenshots_dir, file)
            excel_files.append((file_path, file))
    
    if not excel_files:
        print("❌ No Excel files found")
        return
    
    # Get the most recent file
    latest_file = max(excel_files, key=lambda x: os.path.getctime(x[0]))
    excel_path, filename = latest_file
    
    print(f"📁 Found: {filename}")
    print(f"📁 Path: {excel_path}")
    
    # Create PDF path
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    pdf_path = f"screenshots/latest_pdf_{timestamp}.pdf"
    
    print(f"🔄 Converting to PDF...")
    
    # Try LibreOffice first
    try:
        cmd = [
            'libreoffice',
            '--headless',
            '--convert-to', 'pdf',
            '--outdir', 'screenshots',
            excel_path
        ]
        
        print("Trying LibreOffice...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # Find the created PDF
            expected_pdf = excel_path.replace('.xlsx', '.pdf')
            if os.path.exists(expected_pdf):
                os.rename(expected_pdf, pdf_path)
                print(f"✅ PDF created: {pdf_path}")
                return
            else:
                print("❌ PDF file not found after conversion")
        else:
            print(f"❌ LibreOffice failed: {result.stderr}")
    except Exception as e:
        print(f"❌ LibreOffice error: {str(e)}")
    
    # Try PowerShell as fallback
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
        """
        
        with open("temp_convert.ps1", "w") as f:
            f.write(ps_script)
        
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", "temp_convert.ps1"], timeout=60)
        os.remove("temp_convert.ps1")
        
        if os.path.exists(pdf_path):
            print(f"✅ PDF created: {pdf_path}")
            return
        else:
            print("❌ PowerShell conversion failed")
    except Exception as e:
        print(f"❌ PowerShell error: {str(e)}")
    
    print("\n❌ All conversion methods failed")
    print("Try opening Excel manually and pressing Ctrl+P")

if __name__ == "__main__":
    main()
