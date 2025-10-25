# Test API Script - Excel Download Version

## Overview
Updated test script for the PortOptimizer Excel Download API. This script tests all the new Excel download functionality instead of screenshots.

## What's Changed

### Updated Endpoints:
- `POST /excel/now` - Download Excel report immediately
- `GET /excel/<date>` - Get Excel report for specific date  
- `GET /excel/range` - Get Excel reports for date range
- `GET /download/<filename>` - Download files directly

### Updated Functions:
- `test_download_excel_now()` - Tests immediate Excel download
- `test_get_excel()` - Tests getting Excel by date
- `test_get_excel_range()` - Tests getting Excel range
- `test_download_file()` - Tests direct file download

## Usage

### 1. Start the API Server
```bash
python app.py
```

### 2. Run the Test Script
```bash
python test_api.py
```

### 3. Follow the Prompts
The script will guide you through testing:
- Basic API connectivity
- Excel download functionality
- File retrieval
- Admin functions

## Test Flow

1. **Basic Tests** - Root endpoint, status
2. **Excel Download** - Immediate Excel report download
3. **File Retrieval** - Get Excel reports by date
4. **Download Test** - Direct file download
5. **Admin Functions** - Frequency changes, password validation

## Expected Results

### Successful Excel Download:
```json
{
  "success": true,
  "message": "Excel report downloaded successfully",
  "filename": "2025-01-15_12-00-00.xlsx"
}
```

### Successful Excel Retrieval:
```json
{
  "success": true,
  "date": "2025-01-15",
  "filename": "2025-01-15_12-00-00.xlsx",
  "download_url": "http://localhost:5000/download/2025-01-15_12-00-00.xlsx",
  "message": "Excel report found for 2025-01-15"
}
```

## Configuration

Update these variables in the script:
- `BASE_URL` - API server URL (default: http://localhost:5000)
- `ADMIN_PASSWORD` - Admin password for protected endpoints

## Notes

- Excel downloads take ~2 minutes to complete
- Files are saved in the `downloads/` directory
- PDF conversion happens automatically
- Separator lines are added to Excel files
- All files use timestamp naming

## Troubleshooting

### Connection Error:
```
❌ Error: Could not connect to the API
Make sure the Flask app is running on http://localhost:5000
```

**Solution:** Start the API server with `python app.py`

### Excel Download Fails:
- Check credentials in system settings
- Verify portal access
- Check browser automation setup

### File Not Found:
- Run Excel download test first
- Check downloads directory
- Verify file naming convention
