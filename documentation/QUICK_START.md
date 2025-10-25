# Quick Start Guide

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Start the API

```bash
python app.py
```

You should see:
```
==================================================
PortOptimizer Screenshot API
==================================================
Screenshot frequency: 24.0 hours
Screenshots directory: screenshots
Scheduler started
==================================================
```

The API is now running on `http://localhost:5000`

## Step 3: Test the API

### Option A: Use the Test Script
```bash
python test_api.py
```

### Option B: Manual Testing with cURL

**1. Check API Status:**
```bash
curl http://localhost:5000/status
```

**2. Take a Screenshot Now (requires admin password):**
```bash
curl -X POST http://localhost:5000/screenshot/now \
  -H "Content-Type: application/json" \
  -d "{\"admin_password\":\"YB02Ss3JJdk\"}"
```

This will take about 2 minutes as it:
- Navigates to the portal
- Logs in
- Waits for page to load
- Takes a screenshot

**3. Download Today's Screenshot:**
```bash
curl http://localhost:5000/screenshot/2024-10-23 --output screenshot.png
```
(Replace `2024-10-23` with today's date)

**4. Download Last 5 Screenshots as ZIP:**
```bash
curl "http://localhost:5000/screenshots/range?last_n=5" --output screenshots.zip
```

**5. Change Screenshot Frequency to Every 12 Hours:**
```bash
curl -X POST http://localhost:5000/admin/frequency \
  -H "Content-Type: application/json" \
  -d "{\"admin_password\":\"YB02Ss3JJdk\",\"frequency_hours\":12}"
```

## Default Configuration

- **Admin Password**: `YB02Ss3JJdk`
- **Portal Username**: `sara@fouroneone.io`
- **Portal Password**: `Ss925201!`
- **Screenshot Frequency**: 24 hours (once per day)

## Important Notes

1. **First Screenshot**: The scheduler will take the first screenshot after 24 hours (or whatever frequency is set). Use `/screenshot/now` to take an immediate screenshot.

2. **Browser Visibility**: By default, the browser will be visible during screenshot capture. To run headless:
   - Open `automation.py`
   - Uncomment line: `chrome_options.add_argument('--headless=new')`

3. **Chrome Requirement**: Make sure Chrome browser is installed on your system.

4. **Screenshot Time**: Each screenshot takes approximately 2 minutes due to wait times for page loading and authentication.

5. **Storage**: Screenshots are stored in the `screenshots/` folder with timestamp naming: `YYYY-MM-DD_HH-MM-SS.png`

## Troubleshooting

**Problem**: "ChromeDriver not found"
- **Solution**: Update Selenium: `pip install --upgrade selenium`

**Problem**: "Connection refused"
- **Solution**: Make sure the API is running (`python app.py`)

**Problem**: "No screenshot found"
- **Solution**: Take a screenshot first using `/screenshot/now`

**Problem**: Screenshots failing
- **Solution**: 
  1. Check if Chrome is installed
  2. Verify portal credentials are correct
  3. Check if portal URL is accessible
  4. Look at console logs for specific errors

## Next Steps

- Set up the API to run as a service/daemon for continuous operation
- Configure a reverse proxy (nginx) for production deployment
- Set up HTTPS with SSL certificates
- Change default admin password
- Configure firewall rules

## Production Deployment

For production, consider:
1. Using environment variables for sensitive data
2. Running behind a reverse proxy
3. Enabling HTTPS
4. Setting up monitoring and logging
5. Running the browser in headless mode
6. Using a process manager like `supervisord` or `systemd`

## API Documentation

See `README.md` for complete API documentation.


