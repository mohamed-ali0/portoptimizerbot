# Changelog

## Version 2.0.0 - API Response Changes & Auto-Retry

### 🎯 Major Changes

#### 1. **Public Download Links** (Breaking Change)
All screenshot endpoints now return JSON with download URLs instead of serving files directly.

**Before:**
```bash
# Directly downloads file
curl http://localhost:5000/screenshot/2024-10-23 --output screenshot.png
```

**After:**
```bash
# Returns JSON with download link
curl http://localhost:5000/screenshot/2024-10-23
# Response:
{
  "success": true,
  "download_url": "http://localhost:5000/download/2024-10-23_15-30-00.png",
  "filename": "2024-10-23_15-30-00.png"
}

# Then download using the URL
curl "http://localhost:5000/download/2024-10-23_15-30-00.png" --output screenshot.png
```

#### 2. **Automatic Retry on Failure**
Scheduled screenshots now automatically retry after 5 minutes if they fail.

**Behavior:**
- Screenshot scheduled at 2:00 PM
- Screenshot fails at 2:00 PM
- System automatically schedules retry at 2:05 PM
- Retry happens at 2:05 PM
- If successful, next regular screenshot at 2:00 PM next day
- If still fails, another retry at 2:10 PM

**Console Output:**
```
[2024-10-24 14:00:00] Taking scheduled screenshot...
[2024-10-24 14:02:30] Screenshot failed: Connection timeout
[2024-10-24 14:02:30] Scheduling retry in 5 minutes...
[2024-10-24 14:07:30] Taking scheduled screenshot...
[2024-10-24 14:10:00] Screenshot taken successfully: 2024-10-24_14-10-00.png
```

#### 3. **New /download Endpoint**
Added dedicated endpoint for downloading files.

**Endpoint:** `GET /download/<filename>`

**Purpose:**
- Download screenshot PNG files
- Download ZIP files
- Supports any file in screenshots/ directory

**Example:**
```bash
curl http://localhost:5000/download/2024-10-23_15-30-00.png --output screenshot.png
curl http://localhost:5000/download/screenshots_20241024_153000.zip --output archive.zip
```

### 📋 Updated API Responses

#### GET /screenshot/<date>

**Old Response:** Direct file download

**New Response:**
```json
{
  "success": true,
  "date": "2024-10-23",
  "filename": "2024-10-23_15-30-00.png",
  "download_url": "http://localhost:5000/download/2024-10-23_15-30-00.png",
  "message": "Screenshot found for 2024-10-23"
}
```

#### GET /screenshots/range

**Old Response:** Direct ZIP download

**New Response:**
```json
{
  "success": true,
  "zip_filename": "screenshots_20241024_153000.zip",
  "download_url": "http://localhost:5000/download/screenshots_20241024_153000.zip",
  "screenshot_count": 5,
  "screenshots": [
    "2024-10-20_14-30-00.png",
    "2024-10-21_14-30-00.png",
    "2024-10-22_14-30-00.png",
    "2024-10-23_14-30-00.png",
    "2024-10-24_14-30-00.png"
  ],
  "message": "ZIP file created with 5 screenshot(s)"
}
```

### 🔄 Migration Guide

#### For API Consumers

**Step 1:** Update your code to handle JSON responses

```python
# OLD CODE
response = requests.get('http://localhost:5000/screenshot/2024-10-23')
with open('screenshot.png', 'wb') as f:
    f.write(response.content)

# NEW CODE
response = requests.get('http://localhost:5000/screenshot/2024-10-23')
data = response.json()
if data['success']:
    download_url = data['download_url']
    file_response = requests.get(download_url)
    with open('screenshot.png', 'wb') as f:
        f.write(file_response.content)
```

**Step 2:** Use the `/download` endpoint directly

```python
# BETTER APPROACH
response = requests.get('http://localhost:5000/screenshot/2024-10-23')
data = response.json()
if data['success']:
    filename = data['filename']
    file_response = requests.get(f'http://localhost:5000/download/{filename}')
    with open(filename, 'wb') as f:
        f.write(file_response.content)
```

### 🆕 New Features

1. **Public Download Links**
   - All responses include full download URLs
   - Easy to share and bookmark
   - RESTful API design

2. **Auto-Retry Logic**
   - Automatic retry after 5 minutes on failure
   - Works for scheduled screenshots only
   - Logged in console with timestamps

3. **Enhanced Postman Collection**
   - Automated tests for all endpoints
   - Environment variables for easy testing
   - Chain requests using saved variables

4. **Better Error Handling**
   - Clear error messages in JSON responses
   - Proper HTTP status codes
   - Detailed logging for debugging

### 📁 New Files

- **PortOptimizer_API.postman_environment.json** - Postman environment with variables
- **POSTMAN_GUIDE.md** - Complete guide for using Postman collection
- **CHANGELOG.md** - This file

### 📝 Updated Files

- **app.py** - Updated endpoints to return JSON with download links
- **README.md** - Updated with new API response formats
- **PortOptimizer_API.postman_collection.json** - Added tests and updated requests

### ⚠️ Breaking Changes

1. **Screenshot Endpoints Return JSON**
   - `/screenshot/<date>` now returns JSON instead of file
   - `/screenshots/range` now returns JSON instead of ZIP

2. **Download Flow Changed**
   - Two-step process: Get metadata → Download file
   - Use new `/download/<filename>` endpoint

### ✅ Backward Compatibility

The following endpoints remain unchanged:
- `POST /screenshot/now` - Still returns JSON
- `POST /admin/frequency` - Still returns JSON
- `POST /admin/credentials` - Still returns JSON
- `POST /admin/cleanup` - Still returns JSON
- `GET /status` - Still returns JSON

### 🐛 Bug Fixes

- Fixed issue where ZIP files were not cleaned up after download
- Improved error handling in scheduled tasks
- Better logging for screenshot failures

### 🔮 Future Improvements

Potential features for next version:
- Webhook notifications on screenshot completion
- S3/cloud storage integration
- Screenshot thumbnails
- REST API versioning
- Rate limiting

### 📊 Performance

- No performance impact from JSON responses
- Retry logic runs in background (no blocking)
- Download endpoint uses efficient file streaming

### 🧪 Testing

Updated test_api.py to work with new response format:
```python
# Test new response format
response = requests.get('http://localhost:5000/screenshot/2024-10-23')
data = response.json()
assert 'download_url' in data
assert data['success'] == True
```

### 📚 Documentation Updates

All documentation updated to reflect new API design:
- README.md - Complete API reference
- POSTMAN_GUIDE.md - Postman usage guide
- QUICK_START.md - Quick start examples

---

## Upgrade Instructions

1. **Stop the API**
   ```bash
   # Press Ctrl+C to stop
   ```

2. **Pull latest code**
   ```bash
   git pull origin main
   ```

3. **Restart the API**
   ```bash
   python app.py
   ```

4. **Update your client code**
   - Follow migration guide above
   - Test with new response format

5. **Import new Postman collection**
   - Import updated collection
   - Import environment file
   - Run tests to verify

---

## Support

For questions or issues:
1. Check **POSTMAN_GUIDE.md** for testing examples
2. Review **README.md** for complete API documentation
3. Check console logs for detailed error messages

---

**Release Date:** October 24, 2025
**API Version:** 2.0.0

