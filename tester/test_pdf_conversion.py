import os
import subprocess
from datetime import datetime

def test_pdf_conversion():
    """Test PDF conversion with the existing Excel file"""
    
    # Find the most recent Excel file
    downloads_dir = "downloads"
    if not os.path.exists(downloads_dir):
        print("❌ Downloads directory not found")
        return False
    
    excel_files = []
    for filename in os.listdir(downloads_dir):
        if filename.endswith(('.xlsx', '.xls')) and not filename.startswith('~$'):
            excel_files.append(filename)
    
    if not excel_files:
        print("❌ No Excel files found in downloads directory")
        return False
    
    # Get the most recent file
    latest_excel = max(excel_files, key=lambda x: os.path.getctime(os.path.join(downloads_dir, x)))
    excel_path = os.path.join(downloads_dir, latest_excel)
    
    print(f"✅ Found Excel file: {latest_excel}")
    
    # Create pdfs directory
    pdfs_dir = os.path.join("downloads", "pdfs")
    os.makedirs(pdfs_dir, exist_ok=True)
    
    # Convert to PDF
    pdf_filename = latest_excel.replace('.xlsx', '.pdf').replace('.xls', '.pdf')
    pdf_path = os.path.join(pdfs_dir, pdf_filename)
    
    print(f"Converting to PDF: {pdf_path}")
    
    # Create PowerShell script
    ps_script = f'''
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    
    try {{
        $workbook = $excel.Workbooks.Open('{os.path.abspath(excel_path)}')
        $worksheet = $workbook.Worksheets.Item(1)
        
        # Add borders to all cells with data
        $usedRange = $worksheet.UsedRange
        if ($usedRange) {{
            $usedRange.Borders.LineStyle = 1  # xlContinuous
            $usedRange.Borders.Weight = 1     # xlThin
            # Set gray color for all border sides
            $usedRange.Borders.Item(7).Color = 12632256  # xlEdgeLeft - Light gray
            $usedRange.Borders.Item(8).Color = 12632256  # xlEdgeTop - Light gray  
            $usedRange.Borders.Item(9).Color = 12632256  # xlEdgeBottom - Light gray
            $usedRange.Borders.Item(10).Color = 12632256 # xlEdgeRight - Light gray
        }}
        
        # Set to Legal landscape
        $worksheet.PageSetup.Orientation = 2  # xlLandscape
        $worksheet.PageSetup.PaperSize = 5     # xlPaperLegal
        
        # Export to PDF
        $pdf_path = '{os.path.abspath(pdf_path)}'
        $workbook.ExportAsFixedFormat(0, $pdf_path)
        
        $workbook.Close()
        $excel.Quit()
        
        Write-Host "PDF created: $pdf_path"
    }} catch {{
        Write-Host "Error: $_"
        $excel.Quit()
    }}
    '''
    
    # Write PowerShell script to file
    with open('temp.ps1', 'w') as f:
        f.write(ps_script)
    
    try:
        # Run PowerShell script
        result = subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'temp.ps1'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ PDF conversion successful!")
            print(f"📄 PDF created: {pdf_path}")
            return True
        else:
            print(f"❌ PowerShell error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Conversion timed out")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists('temp.ps1'):
            os.remove('temp.ps1')

if __name__ == "__main__":
    print("=" * 50)
    print("TEST PDF CONVERSION")
    print("=" * 50)
    
    test_pdf_conversion()