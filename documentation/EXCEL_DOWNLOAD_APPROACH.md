# Excel Download Approach

## Overview
The system has been updated to download Excel reports instead of taking screenshots. This approach is more reliable and provides better data quality.

## New Flow

### 1. **Login to Portal**
- Navigate to PortOptimizer portal
- Enter credentials and login
- Wait for page to load

### 2. **Click Return Signal Tab**
- Find and click the "Return Signal" tab
- Wait 15 seconds for the page to load

### 3. **Download Excel Report**
- Find and click the download button
- Wait for Excel file to download
- Save with timestamp filename

### 4. **Add Separator Lines**
- Load the Excel file using openpyxl
- Add visible borders to all cells
- Save the formatted Excel file

### 5. **Convert to PDF**
- Convert Excel to PDF in landscape legal format
- Ensure all separator lines are visible
- Save PDF for printing

## API Endpoints

### Updated Endpoints:
- `POST /excel/now` - Download Excel report immediately
- `GET /excel/<date>` - Get Excel report for specific date
- `GET /excel/range` - Get Excel reports for date range

### New Features:
- **Separator Lines**: All Excel cells get visible borders
- **PDF Conversion**: Excel files are converted to PDF
- **Landscape Legal**: PDFs are formatted for legal paper size
- **Auto-retry**: Failed downloads retry in 5 minutes

## File Structure

```
project/
├── downloads/           # Excel files
├── downloads/           # PDF files (converted)
├── automation.py        # Updated for Excel download
├── app.py              # Updated API endpoints
└── requirements.txt    # Added pandas, openpyxl
```

## Dependencies Added

```txt
pandas==2.1.3      # Excel file processing
openpyxl==3.1.2    # Excel file manipulation
```

## Benefits

1. **More Reliable**: No extension dependencies
2. **Better Quality**: Excel data is more accurate than screenshots
3. **Easier Processing**: Excel files are easier to work with
4. **Visible Separators**: All cells have clear borders
5. **PDF Ready**: Automatic conversion to print-ready PDF

## Testing

Run the test script to verify functionality:

```bash
python test_excel_download.py
```

## Usage

### Download Excel Report Now:
```bash
curl -X POST http://localhost:5000/excel/now \
  -H "Content-Type: application/json" \
  -d '{"admin_password": "admin123"}'
```

### Get Excel Report for Date:
```bash
curl http://localhost:5000/excel/2025-01-15
```

## Configuration

The system uses the same configuration as before:
- Username/password in system settings
- Scheduler frequency settings
- Admin password for immediate downloads

## Notes

- Excel files are saved in `downloads/` directory
- PDF files are saved alongside Excel files
- All files use timestamp naming
- Separator lines are added automatically
- PDFs are formatted for landscape legal printing
