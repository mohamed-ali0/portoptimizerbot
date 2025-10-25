@echo off
echo ========================================
echo EXCEL TO PDF CONVERSION
echo ========================================
echo This will open Excel and print to PDF
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

REM Create VBS script to open Excel and print to PDF
echo Set objExcel = CreateObject("Excel.Application") > temp_print.vbs
echo objExcel.Visible = True >> temp_print.vbs
echo Set objWorkbook = objExcel.Workbooks.Open("%~dp0%excel_file%") >> temp_print.vbs
echo Set objWorksheet = objWorkbook.ActiveSheet >> temp_print.vbs
echo objWorksheet.PageSetup.Orientation = 2 >> temp_print.vbs
echo objWorksheet.PageSetup.PaperSize = 5 >> temp_print.vbs
echo objWorkbook.ExportAsFixedFormat 0, "%~dp0screenshots\output.pdf" >> temp_print.vbs
echo objWorkbook.Close >> temp_print.vbs
echo objExcel.Quit >> temp_print.vbs

echo Opening Excel and converting to PDF...
cscript //nologo temp_print.vbs

REM Clean up
del temp_print.vbs

echo.
echo ========================================
echo CONVERSION COMPLETE
echo ========================================
echo Check screenshots\output.pdf
echo ========================================
pause
