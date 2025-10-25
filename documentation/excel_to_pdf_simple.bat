@echo off
echo ========================================
echo SIMPLE EXCEL TO PDF CONVERSION
echo ========================================
echo This will convert Excel to Legal Landscape PDF
echo ========================================

REM Find the most recent Excel file
for /f "delims=" %%i in ('dir /b /o-d screenshots\*.xlsx 2^>nul') do (
    set "excel_file=screenshots\%%i"
    goto :found
)

echo No Excel files found in screenshots directory
pause
exit /b 1

:found
echo Found Excel file: %excel_file%

REM Create VBS script to convert to PDF
echo Set objExcel = CreateObject("Excel.Application") > temp_convert.vbs
echo objExcel.Visible = False >> temp_convert.vbs
echo objExcel.DisplayAlerts = False >> temp_convert.vbs
echo Set objWorkbook = objExcel.Workbooks.Open("%~dp0%excel_file%") >> temp_convert.vbs
echo Set objWorksheet = objWorkbook.ActiveSheet >> temp_convert.vbs
echo objWorksheet.PageSetup.Orientation = 2 >> temp_convert.vbs
echo objWorksheet.PageSetup.PaperSize = 5 >> temp_convert.vbs
echo objWorkbook.ExportAsFixedFormat 0, "%~dp0screenshots\simple_output.pdf" >> temp_convert.vbs
echo objWorkbook.Close >> temp_convert.vbs
echo objExcel.Quit >> temp_convert.vbs

echo Converting Excel to PDF...
cscript //nologo temp_convert.vbs

REM Clean up
del temp_convert.vbs

echo.
echo ========================================
echo CONVERSION COMPLETE
echo ========================================
echo Check screenshots\simple_output.pdf
echo ========================================
pause
