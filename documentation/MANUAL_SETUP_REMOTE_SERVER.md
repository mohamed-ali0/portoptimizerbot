# Manual Extension Setup for Remote Server

## Quick Setup Guide (5 Minutes)

Since the `.crx` file doesn't work on your remote server, install the extension manually once and it will persist forever.

---

## Step 1: Install Extension Manually

### 1. Stop Flask app if running
Press `CTRL+C` in the terminal running `app.py`

### 2. Open Chrome with the profile used by automation

Open PowerShell and run:
```powershell
cd "C:\Users\Mohamed Ali\Downloads\portoptimizer_screenshot_api"
start chrome --user-data-dir=chrome_profile --profile-directory=Default
```

This opens Chrome using the SAME profile that automation uses.

### 3. Install GoFullPage extension

In the Chrome window that just opened:
1. Go to: https://chromewebstore.google.com/detail/gofull-page-full-page-scr/fdpohaocaechififmbbbbbknoalclacl
2. Click **"Add to Chrome"**
3. Click **"Add extension"** when prompted
4. Grant any permissions requested

### 4. Configure keyboard shortcut

⚠️ **IMPORTANT**: Use `Ctrl+Shift+K` to avoid conflicts with browser shortcuts

In the same Chrome window:
1. Go to: `chrome://extensions/shortcuts`
2. Find **"GoFullPage - Full Page Screen Capture"**
3. Click in the shortcut field next to "Capture Entire Page"
4. Press: **Ctrl+Shift+K** (exactly these keys)
5. Make sure it says "Ctrl+Shift+K" in the field

**Why Ctrl+Shift+K?**
- ✅ Rarely used by browsers
- ✅ Works on Chrome, Brave, Edge, etc.
- ✅ No conflicts with Windows shortcuts
- ❌ Alt+Shift+P conflicts with "New Tab Group"

### 5. Grant download permissions (Important!)

Still in Chrome:
1. Click the GoFullPage icon in the toolbar (puzzle piece icon → GoFullPage)
2. Take a test screenshot on any page
3. Click **"Download image"**
4. If a popup appears asking "Allow downloads?", click **"Allow"**
5. Delete the test screenshot

### 6. Close Chrome completely

Close ALL Chrome windows. Make sure Chrome is not running in Task Manager.

---

## Step 2: Start Flask App

Now start the app:
```powershell
python app.py
```

The automation will:
- ✅ Use the chrome_profile where extension is installed
- ✅ Extension loads automatically (no .crx needed)
- ✅ Ctrl+Shift+K triggers screenshot
- ✅ Works on remote server and local machine

---

## Testing

Test that it works:
```powershell
# In a new PowerShell window
curl -X POST http://localhost:5000/screenshot/now `
  -H "Content-Type: application/json" `
  -d '{\"admin_password\":\"YB02Ss3JJdk\"}'
```

Watch the console for:
```
[timestamp] Using extension from chrome_profile (no .crx needed)
[timestamp] Chrome window forcefully brought to front and maximized
[timestamp] Triggering GoFullPage with Ctrl+Shift+K...
[timestamp] System keyboard input sent
[timestamp] Waiting for extension to capture and open new tab...
[timestamp] Screenshot saved: 2025-10-24_12-30-45.png
```

---

## Troubleshooting

### Shortcut doesn't work
1. Open Chrome manually with the profile
2. Go to `chrome://extensions/shortcuts`
3. Verify GoFullPage shortcut is set to **Ctrl+Shift+K**
4. Try pressing it manually - it should trigger screenshot
5. If it doesn't work even manually, try a different shortcut:
   - **Alt+Shift+S** (screenshot)
   - **Ctrl+Shift+F** (fullpage)
   - **Alt+Shift+F** (capture)

### Extension not found
```powershell
# Open Chrome with profile and check extensions
start chrome --user-data-dir=chrome_profile --profile-directory=Default
# Then go to chrome://extensions/
```

### Still using .crx?
Make sure you updated `automation.py` with the changes from the guide.
