# PortOptimizer Screenshot API

A Flask-based API that automates login to the PortOptimizer portal and takes full-page screenshots on a scheduled basis.

## Features

- 🤖 **Automated Login**: Uses Selenium to automatically log in to the portal
- 📸 **Scheduled Screenshots**: Takes full-page screenshots at configurable intervals (default: 24 hours)
- 🔄 **Auto-Retry**: If scheduled screenshot fails, automatically retries after 5 minutes
- 🔐 **Secure Admin Endpoints**: Protected endpoints for system management
- 📦 **Bulk Download**: Download multiple screenshots as a ZIP file
- 🔗 **Public Download Links**: All endpoints return JSON with public download URLs
- ⚙️ **Configurable Settings**: Change frequency and login credentials on-the-fly

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- ChromeDriver (automatically managed by Selenium 4.6+)

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Run the application**:
```bash
python app.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### 1. Get Screenshot by Date
**Endpoint**: `GET /screenshot/<date>`

**Description**: Get screenshot metadata and download link for a specific date.

**Parameters**:
- `date` (path): Date in format `YYYY-MM-DD`

**Response**:
```json
{
  "success": true,
  "date": "2024-10-23",
  "filename": "2024-10-23_15-30-00.png",
  "download_url": "http://localhost:5000/download/2024-10-23_15-30-00.png",
  "message": "Screenshot found for 2024-10-23"
}
```

**Example**:
```bash
curl http://localhost:5000/screenshot/2024-10-23
```

Then download using the URL from response:
```bash
curl http://localhost:5000/download/2024-10-23_15-30-00.png --output screenshot.png
```

---

### 2. Get Screenshot Range
**Endpoint**: `GET /screenshots/range`

**Description**: Get download link for ZIP file containing multiple screenshots.

**Query Parameters** (choose one):
- **Option A**: Date range
  - `start_date`: Start date (YYYY-MM-DD)
  - `end_date`: End date (YYYY-MM-DD)
- **Option B**: Last N screenshots
  - `last_n`: Number of most recent screenshots

**Response**:
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

**Examples**:
```bash
# Get screenshots between two dates
curl "http://localhost:5000/screenshots/range?start_date=2024-10-20&end_date=2024-10-23"

# Get last 5 screenshots
curl "http://localhost:5000/screenshots/range?last_n=5"

# Then download using the URL from response
curl "http://localhost:5000/download/screenshots_20241024_153000.zip" --output screenshots.zip
```

---

### 3. Download File
**Endpoint**: `GET /download/<filename>`

**Description**: Download a screenshot or ZIP file directly.

**Parameters**:
- `filename` (path): Filename from previous API responses

**Example**:
```bash
curl http://localhost:5000/download/2024-10-23_15-30-00.png --output screenshot.png
curl http://localhost:5000/download/screenshots_20241024_153000.zip --output screenshots.zip
```

---

### 4. Change Screenshot Frequency
**Endpoint**: `POST /admin/frequency`

**Description**: Change how often screenshots are taken.

**Body**:
```json
{
    "admin_password": "YB02Ss3JJdk",
    "frequency_hours": 12
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/admin/frequency \
  -H "Content-Type: application/json" \
  -d '{"admin_password":"YB02Ss3JJdk","frequency_hours":12}'
```

---

### 5. Update Login Credentials
**Endpoint**: `POST /admin/credentials`

**Description**: Update the portal login credentials.

**Body**:
```json
{
    "admin_password": "YB02Ss3JJdk",
    "username": "new_username@example.com",
    "password": "new_password"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/admin/credentials \
  -H "Content-Type: application/json" \
  -d '{"admin_password":"YB02Ss3JJdk","username":"sara@fouroneone.io","password":"Ss925201!"}'
```

---

### 6. Cleanup Screenshots
**Endpoint**: `POST /admin/cleanup`

**Description**: Delete all screenshots from the system.

**Body**:
```json
{
    "admin_password": "YB02Ss3JJdk"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/admin/cleanup \
  -H "Content-Type: application/json" \
  -d '{"admin_password":"YB02Ss3JJdk"}'
```

---

### 7. Take Screenshot Now
**Endpoint**: `POST /screenshot/now`

**Description**: Trigger an immediate screenshot (doesn't affect schedule).

**Body**:
```json
{
    "admin_password": "YB02Ss3JJdk"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/screenshot/now \
  -H "Content-Type: application/json" \
  -d '{"admin_password":"YB02Ss3JJdk"}'
```

---

### 8. System Status
**Endpoint**: `GET /status`

**Description**: Get current system status and configuration.

**Example**:
```bash
curl http://localhost:5000/status
```

**Response**:
```json
{
    "success": true,
    "frequency_hours": 24,
    "username": "sara@fouroneone.io",
    "total_screenshots": 15,
    "last_screenshot": "2024-10-23_14-30-00.png",
    "scheduler_running": true
}
```

---

## File Structure

```
portoptimizer_screenshot_api/
├── app.py                     # Main Flask application
├── automation.py              # Selenium automation script
├── system_settings.py         # Settings manager
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── system_settings.json       # System configuration (auto-generated)
└── screenshots/               # Screenshot storage (auto-generated)
    ├── 2024-10-23_14-30-00.png
    ├── 2024-10-24_14-30-00.png
    └── ...
```

## Configuration

The `system_settings.json` file stores:
- Screenshot frequency (in hours)
- Admin password
- Portal login credentials

**Default values**:
- Frequency: 24 hours (once per day)
- Admin password: `YB02Ss3JJdk`
- Username: `sara@fouroneone.io`
- Password: `Ss925201!`

## Screenshot Naming Convention

Screenshots are saved with timestamp format: `YYYY-MM-DD_HH-MM-SS.png`

Example: `2024-10-23_14-30-00.png`

## Automation Flow

1. Navigate to https://tower.portoptimizer.com/
2. Wait 30 seconds for page load
3. Click "Log In" button
4. Wait 30 seconds for login page
5. Enter username
6. Click "Next" button
7. Wait 15 seconds
8. Enter password
9. Click "Verify" button
10. Wait 30 seconds for dashboard
11. Take full-page screenshot
12. Save with timestamp

## Troubleshooting

### ChromeDriver Issues
If you encounter ChromeDriver issues, make sure:
- Chrome browser is installed
- You have the latest version of Selenium
- Your Chrome version matches the ChromeDriver version

### Screenshots Not Being Taken
- Check the console logs for errors
- Verify the portal credentials are correct
- Ensure the portal URL is accessible
- Check if the scheduler is running: `GET /status`

### Admin Password Not Working
The default admin password is `YB02Ss3JJdk`. If you've changed it and forgot it, you can:
1. Delete `system_settings.json`
2. Restart the application (it will recreate with defaults)

## Security Notes

⚠️ **Important**: 
- Change the default admin password in production
- Keep `system_settings.json` secure (contains credentials)
- Consider using environment variables for sensitive data
- Use HTTPS in production environments

## Development

To run in development mode with auto-reload:
```python
# In app.py, change:
app.run(host='0.0.0.0', port=5000, debug=True)
```

To run headless (without browser UI):
```python
# In automation.py, uncomment:
chrome_options.add_argument('--headless=new')
```

## License

This project is provided as-is for internal use.

## Support

For issues or questions, please contact the development team.

