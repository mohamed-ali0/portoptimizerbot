# Quick Start Guide for Remote Server

## Problem: Extension keyboard shortcut conflict
- ❌ **Alt+Shift+P** triggers browser's "New Tab Group" instead of extension
- ✅ **Ctrl+Shift+K** is a safe shortcut that doesn't conflict

## Solution: Updated keyboard shortcut to Ctrl+Shift+K

---

## 🚀 Setup on Remote Server (5 Minutes)

### Step 1: Install Extension Manually (One Time Only)

Since `.crx` files may not work on remote servers, install the extension manually once:

```powershell
# Stop Flask app if running (Ctrl+C)

# Open Chrome with the automation profile
cd "C:\Users\Mohamed Ali\Downloads\portoptimizer_screenshot_api"
start chrome --user-data-dir=chrome_profile --profile-directory=Default
```

**In the Chrome window that opens:**

1. **Install GoFullPage**:
   - Go to: https://chromewebstore.google.com/detail/gofull-page-full-page-scr/fdpohaocaechififmbbbbbknoalclacl
   - Click "Add to Chrome" → "Add extension"

2. **Set Keyboard Shortcut**:
   - Go to: `chrome://extensions/shortcuts`
   - Find "GoFullPage - Full Page Screen Capture"
   - Click in the shortcut field next to "Capture Entire Page"
   - Press: **Ctrl+Shift+K**
   - Verify it shows "Ctrl+Shift+K"

3. **Grant Download Permission** (Important!):
   - Click GoFullPage icon in toolbar
   - Take a test screenshot on any page
   - Click "Download image"
   - If popup appears: Click "Allow"
   - Delete the test screenshot

4. **Close Chrome completely**

---

### Step 2: Verify Setup

Run the test script to verify everything works:

```powershell
python test_extension_shortcut.py
```

**Expected output:**
```
[1/4] Starting Chrome with profile...
   [OK] Chrome started
[2/4] Navigating to test page...
   [OK] Page loaded
[3/4] Checking if extension is installed...
   [OK] GoFullPage extension found!
   [OK] Keyboard shortcut Ctrl+Shift+K is configured!
[4/4] Testing keyboard shortcut Ctrl+Shift+K...
   [OK] Keyboard shortcut sent (Ctrl+Shift+K)
   Waiting 10 seconds for extension to respond...
   Tabs after shortcut: 2

SUCCESS! Extension keyboard shortcut works!
```

---

### Step 3: Start Flask App

```powershell
python app.py
```

**Expected output:**
```
[timestamp] Using persistent Chrome profile at: chrome_profile
[timestamp] Using extension from chrome_profile (no .crx needed)
...
Next screenshot scheduled for: YYYY-MM-DD HH:MM:SS
 * Running on http://127.0.0.1:5000
```

---

### Step 4: Test Screenshot

In a new PowerShell window:

```powershell
curl -X POST http://localhost:5000/screenshot/now `
  -H "Content-Type: application/json" `
  -d '{\"admin_password\":\"YB02Ss3JJdk\"}'
```

**Watch the Flask console for:**
```
[timestamp] Triggering GoFullPage with keyboard shortcut (Ctrl + Shift + K)...
[timestamp] System keyboard input sent (Ctrl+Shift+K)
[timestamp] Waiting 15 seconds for extension to capture screenshot...
[timestamp] Found and switched to extension tab (2 tabs total)
[timestamp] Download button clicked
[timestamp] Screenshot saved: 2025-10-24_12-30-45.png
```

---

## ✅ What Changed

### 1. Updated Keyboard Shortcut
- **Old**: Alt+Shift+P (conflicted with browser)
- **New**: Ctrl+Shift+K (no conflicts)

### 2. Files Updated
- ✅ `automation.py` - Uses Ctrl+Shift+K now
- ✅ `SETUP_GOFULLPAGE.md` - Documentation updated
- ✅ `MANUAL_SETUP_REMOTE_SERVER.md` - Remote server guide
- ✅ `test_extension_shortcut.py` - New test script
- ✅ `QUICK_START_REMOTE_SERVER.md` - This guide

### 3. No .crx File Needed
- Extension persists in `chrome_profile/` after manual installation
- Automation loads extension from profile automatically
- Works on any server (local, remote, cloud)

---

## 📋 Troubleshooting

### Shortcut doesn't work
```powershell
# Check if shortcut is set correctly
start chrome --user-data-dir=chrome_profile --profile-directory=Default
# Then go to: chrome://extensions/shortcuts
# Verify GoFullPage shows "Ctrl+Shift+K"
```

### Extension not found
```powershell
# Check if extension is installed
start chrome --user-data-dir=chrome_profile --profile-directory=Default
# Then go to: chrome://extensions/
# GoFullPage should be listed and enabled
```

### Still getting "New Tab Group"
This means the extension shortcut isn't configured. Follow Step 1 again.

### Download permission popup blocks download
Follow Step 1.3 to grant permission once - it persists forever.

---

## 🎯 Alternative Shortcuts (If Ctrl+Shift+K doesn't work)

If Ctrl+Shift+K conflicts on your system, try these alternatives:

1. **Alt+Shift+S** (Screenshot)
2. **Ctrl+Shift+F** (Fullpage)
3. **Alt+Shift+F** (Capture)

**To change:**
1. Set new shortcut in `chrome://extensions/shortcuts`
2. Update `automation.py` around line 273:
   ```python
   keyboard.press(Key.ctrl)  # or Key.alt
   keyboard.press(Key.shift)
   keyboard.press('k')  # or 's' or 'f'
   ```

---

## 🌐 Works With All Chromium Browsers

This approach works with:
- ✅ Google Chrome
- ✅ Microsoft Edge
- ✅ Brave Browser
- ✅ Chromium

Just install GoFullPage from each browser's extension store!

---

## 📞 Support

If you encounter issues:
1. Run `python test_extension_shortcut.py` and share output
2. Check Flask console logs
3. Verify extension is installed: `chrome://extensions/`
4. Verify shortcut is set: `chrome://extensions/shortcuts`

---

**You're all set! The automation will now take daily screenshots on your remote server.** 🎉

