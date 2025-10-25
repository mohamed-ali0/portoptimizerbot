import os
import subprocess
import time

def convert_specific_excel():
    """Convert the specific POLA_Empty_Returns Excel file to PDF"""
    
    # The specific file we want to convert (it's in the screenshots directory)
    excel_file = "screenshots/POLA_Empty_Returns_2025-10-26_00-46-48.xlsx"
    
    # Check if file exists
    if not os.path.exists(excel_file):
        print(f"❌ File not found: {excel_file}")
        return False
    
    print(f"✅ Found: {excel_file}")
    print("Converting to PDF...")
    
    # Create PowerShell script
    ps_script = f'''
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    
    try {{
        $workbook = $excel.Workbooks.Open('{os.path.abspath(excel_file)}')
        $worksheet = $workbook.Worksheets.Item(1)
        
        # Add gray borders to all cells with data
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
        $pdf_path = '{os.path.abspath(excel_file.replace(".xlsx", ".pdf"))}'
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
            print("✅ Conversion successful!")
            print(f"📄 PDF created: {excel_file.replace('.xlsx', '.pdf')}")
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
    print("CONVERT SPECIFIC EXCEL FILE")
    print("=" * 50)
    
    convert_specific_excel()
