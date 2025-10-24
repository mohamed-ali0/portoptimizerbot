# Postman Collection Guide

Complete guide for testing the PortOptimizer Screenshot API using Postman.

## 📦 Files Provided

1. **PortOptimizer_API.postman_collection.json** - Collection with all API endpoints
2. **PortOptimizer_API.postman_environment.json** - Environment variables

## 🚀 Quick Setup

### Step 1: Import Collection

1. Open Postman
2. Click **Import** button (top left)
3. Drag and drop `PortOptimizer_API.postman_collection.json`
4. Click **Import**

### Step 2: Import Environment

1. Click **Import** button again
2. Drag and drop `PortOptimizer_API.postman_environment.json`
3. Click **Import**

### Step 3: Activate Environment

1. Click environment dropdown (top right)
2. Select **PortOptimizer API Environment**

### Step 4: Start API Server

```bash
python app.py
```

### Step 5: Test Endpoints

Click **Send** on any request in the collection!

## 🌍 Environment Variables

The environment includes these pre-configured variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `http://localhost:5000` | API base URL |
| `admin_password` | `YB02Ss3JJdk` | Admin password for protected endpoints |
| `current_date` | Auto-generated | Current date for testing |
| `last_screenshot` | Auto-set | Filename from last screenshot |
| `download_url` | Auto-set | Download URL from responses |
| `zip_download_url` | Auto-set | ZIP download URL |

### Changing Environment Variables

1. Click environment dropdown → **PortOptimizer API Environment**
2. Click eye icon to view variables
3. Edit values as needed
4. Click **Save**

## 📋 Request Collection Overview

### 1. **API Info**
- Method: `GET /`
- Returns API information and available endpoints
- No auth required

### 2. **System Status**
- Method: `GET /status`
- Returns current system configuration
- Includes tests for response validation

### 3. **Take Screenshot Now**
- Method: `POST /screenshot/now`
- Triggers immediate screenshot (takes ~2-3 minutes)
- Requires admin password
- Auto-saves `filename` to environment

### 4. **Get Screenshot by Date**
- Method: `GET /screenshot/{{current_date}}`
- Returns download link for specific date
- Auto-saves `download_url` to environment

### 5. **Download File**
- Method: `GET /download/{{last_screenshot}}`
- Downloads the actual file
- Uses filename from previous responses

### 6. **Get Screenshots Range (Date Range)**
- Method: `GET /screenshots/range?start_date=...&end_date=...`
- Returns ZIP download link for date range
- Includes list of screenshots in ZIP

### 7. **Get Screenshots Range (Last N)**
- Method: `GET /screenshots/range?last_n=5`
- Returns ZIP download link for last N screenshots
- Auto-saves `zip_download_url` to environment

### 8. **Change Frequency**
- Method: `POST /admin/frequency`
- Changes screenshot frequency
- Requires admin password

### 9. **Update Login Credentials**
- Method: `POST /admin/credentials`
- Updates portal login credentials
- Requires admin password

### 10. **Cleanup Screenshots**
- Method: `POST /admin/cleanup`
- Deletes all screenshots
- Requires admin password
- ⚠️ Use with caution!

## 🧪 Test Scripts

Each request includes automated tests that run after the response:

### Status Checks
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

### Response Validation
```javascript
pm.test("Response has success field", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('success');
});
```

### Auto-Save Variables
```javascript
pm.test("Response has download_url", function () {
    var jsonData = pm.response.json();
    pm.environment.set("download_url", jsonData.download_url);
});
```

## 🔄 Typical Workflow

### Workflow 1: Take Screenshot and Download

```
1. Take Screenshot Now
   → Wait 2-3 minutes for completion
   → filename saved to {{last_screenshot}}

2. Get Screenshot by Date
   → Returns download link
   → download_url saved to environment

3. Download File
   → Uses {{last_screenshot}} from step 1
   → Downloads actual PNG file
```

### Workflow 2: Get Range of Screenshots

```
1. System Status
   → Check how many screenshots available

2. Get Screenshots Range (Last N)
   → Request last 5 screenshots
   → ZIP file created
   → download_url saved to environment

3. Download File
   → Uses ZIP URL from step 2
   → Downloads ZIP with all screenshots
```

### Workflow 3: Change Configuration

```
1. Change Frequency
   → Update to 12 hours

2. System Status
   → Verify frequency changed

3. Update Login Credentials
   → Update portal credentials
```

## 📝 Response Examples

### Get Screenshot Response
```json
{
  "success": true,
  "date": "2024-10-24",
  "filename": "2024-10-24_15-30-00.png",
  "download_url": "http://localhost:5000/download/2024-10-24_15-30-00.png",
  "message": "Screenshot found for 2024-10-24"
}
```

### Get Range Response
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

## 🎯 Testing Tips

### Test All Endpoints
1. Run entire collection: Click **▶ Run** button
2. Select all requests
3. Click **Run PortOptimizer Screenshot API**
4. View test results

### Use Console
1. Open Postman Console (bottom left)
2. View detailed request/response logs
3. Debug issues

### Save Responses
1. Click **Save Response** button
2. Create example responses
3. Document API behavior

## 🔧 Troubleshooting

### Connection Refused
**Problem**: Cannot connect to API
**Solution**: 
- Make sure Flask app is running: `python app.py`
- Check `base_url` in environment: `http://localhost:5000`

### 404 Not Found
**Problem**: Endpoint not found
**Solution**:
- Check if endpoint exists in Flask app
- Verify URL path in request

### 403 Forbidden
**Problem**: Admin password incorrect
**Solution**:
- Check `admin_password` in environment
- Default: `YB02Ss3JJdk`

### Tests Failing
**Problem**: Automated tests fail
**Solution**:
- Check response structure
- View Console for details
- Verify API is returning expected format

### Environment Variables Not Working
**Problem**: Variables like `{{last_screenshot}}` not replaced
**Solution**:
- Make sure environment is **active** (top right dropdown)
- Run previous requests that set these variables
- Check variable names match exactly

## 📊 Advanced Features

### Pre-request Scripts
Some requests use pre-request scripts to generate dynamic values:

```javascript
// Generate current date
pm.environment.set("current_date", new Date().toISOString().split('T')[0]);
```

### Chain Requests
Use saved environment variables to chain requests:

```
Take Screenshot → Save filename → Download using filename
```

### Collection Runner
Run all requests in sequence:
1. Click **▶ Run** 
2. Select requests to run
3. Set iteration count
4. Click **Run**

## 🎓 Best Practices

1. **Always activate environment** before testing
2. **Run System Status first** to verify API is running
3. **Take Screenshot** before testing download endpoints
4. **Check Console** for debugging
5. **Save responses** for documentation
6. **Use tests** to validate responses automatically

## 📚 Additional Resources

- **README.md** - Complete API documentation
- **QUICK_START.md** - Quick setup guide
- **API Endpoint Docs** - Detailed endpoint descriptions

---

Happy Testing! 🚀

