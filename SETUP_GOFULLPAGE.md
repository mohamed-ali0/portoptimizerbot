# GoFullPage Extension Setup

The application now uses the **GoFullPage** Chrome extension for professional full-page screenshots.

## 📥 How to Get the Extension

### Option 1: Download CRX File (Recommended)

1. **Download GoFullPage CRX file**:
   - Visit: https://chrome-extension-downloader.com/
   - Paste extension URL: `https://chromewebstore.google.com/detail/gofull-page-full-page-scr/fdpohaocaechififmbbbbbknoalclacl`
   - Download the `.crx` file

2. **Place in Project Directory**:
   ```
   portoptimizer_screenshot_api/
   ├── gofullpage.crx          ← Place the file here
   ├── app.py
   ├── automation.py
   └── ...
   ```

3. **Rename the file**:
   - Make sure it's named exactly: `gofullpage.crx`

### Option 2: Pack Extension Manually

1. **Install GoFullPage in Chrome**:
   - Visit: https://chromewebstore.google.com/detail/gofull-page-full-page-scr/fdpohaocaechififmbbbbbknoalclacl
   - Click "Add to Chrome"

2. **Get Extension Files**:
   - Go to `chrome://extensions/`
   - Enable "Developer mode" (top right)
   - Find "GoFullPage - Full Page Screen Capture"
   - Note the extension ID: `fdpohaocaechififmbbbbbknoalclacl`
   - Click "Pack extension"
   - Browse to extension location (usually in `C:\Users\YourName\AppData\Local\Google\Chrome\User Data\Default\Extensions\fdpohaocaechififmbbbbbknoalclacl\`)
   - Pack and save as `gofullpage.crx`

3. **Move to Project**:
   - Copy `gofullpage.crx` to project root directory

## ✅ Verify Installation

Run this command to check if the extension file is found:

```bash
python -c "import os; print('✓ Found' if os.path.exists('gofullpage.crx') else '✗ Not found')"
```

## 🚀 How It Works

When taking a screenshot:

1. ✅ Extension loads automatically when Chrome starts
2. ✅ After login (45 sec wait), page scrolls to top
3. ✅ **Chrome is FORCED to top and fullscreen TWICE** (before capture) using Windows API
4. ✅ System-level keyboard shortcut **Ctrl + Shift + K** is sent via pynput
5. ✅ Extension captures full scrollable page (15 sec wait)
6. ✅ Script finds the new tab opened by extension
7. ✅ Download button is clicked automatically
8. ✅ **Download permission popup is handled** (clicks "Allow" if appears)
9. ✅ Waits 10 seconds for download to complete
10. ✅ Extension tab is closed
11. ✅ Returns to main window
12. ✅ Screenshot saved to `screenshots/` folder with timestamp

## ⌨️ Keyboard Shortcut Setup

**IMPORTANT**: The automation uses **Ctrl + Shift + K** to avoid conflicts with browser shortcuts.

⚠️ **Why not Alt+Shift+P?** That shortcut conflicts with browser's "New Tab Group" feature.

1. Go to `chrome://extensions/shortcuts`
2. Find "GoFullPage - Full Page Screen Capture"
3. Click in the shortcut field next to "Capture Entire Page"
4. Press: **Ctrl+Shift+K** (exactly these keys)
5. Make sure it shows "Ctrl+Shift+K" in the field
6. The automation will send: **Ctrl + Shift + K** as system-level keyboard input

## 📋 Console Output

```
[timestamp] GoFullPage extension loaded
[timestamp] Setting window to fullscreen...
[timestamp] Navigating to portal...
...
[timestamp] Taking full-page screenshot using GoFullPage extension...
[timestamp] Ensuring Chrome window is on top and fullscreen before capture...
[timestamp] Chrome window brought to front and maximized
[timestamp] Chrome window brought to front and maximized  (forced twice)
[timestamp] Triggering GoFullPage with keyboard shortcut (Ctrl + Shift + K)...
[timestamp] System keyboard input sent (Ctrl+Shift+K)
[timestamp] Waiting 15 seconds for extension to capture screenshot...
[timestamp] Looking for extension result tab...
[timestamp] Found and switched to extension tab (2 tabs total)
[timestamp] Looking for download button...
[timestamp] Found download button, file: screencapture-cursor-dashboard-2025-10-24-00_38_12.png
[timestamp] Download button clicked
[timestamp] Checking for download permission popup...
[timestamp] Clicked 'Allow' on permission popup  (or "No permission popup needed")
[timestamp] Waiting 10 seconds for download to complete...
[timestamp] Closing extension tab...
[timestamp] Switched back to main window
[timestamp] Screenshot saved: 2024-10-23_15-30-00.png
```

## ⚠️ Important Notes

1. **Keyboard Shortcut**: Must set **Ctrl+Shift+K** in `chrome://extensions/shortcuts` (avoids conflicts with browser shortcuts like "New Tab Group")

2. **Dependencies Required**: 
   - `pip install pynput==1.7.6` - for system-level keyboard automation
   - `pip install pywin32==306` - for Windows window management

3. **Automatic Window Management**: Script **automatically** forces Chrome to top and fullscreen before screenshot

4. **System-Level Input**: Uses pynput to send real OS keyboard events (indistinguishable from real keyboard)

5. **Headless Mode**: Does NOT work in headless mode. Chrome must be visible.

6. **File Location**: Place `gofullpage.crx` in the **project root directory** (same level as `app.py`)

7. **Filename**: Must be named exactly `gofullpage.crx` (lowercase)

8. **Downloads**: Screenshots download to `screenshots/` folder automatically

9. **First Run**: Extension may show welcome screen first time - this is handled automatically

10. **Windows Only**: pywin32 window forcing works on Windows. For Linux/Mac, window management may differ.

## 🔧 Troubleshooting

### "WARNING: gofullpage.crx not found"
- Check file is in project root directory
- Check filename is exactly `gofullpage.crx`
- Check file permissions (should be readable)

### Keyboard shortcut not working
- Go to `chrome://extensions/shortcuts`
- Verify **Alt+Shift+P** is set for GoFullPage
- Make sure shortcut is "Global" or "In Chrome"
- Check no other extension is using the same shortcut
- Install pynput: `pip install pynput==1.7.6`
- Ensure Chrome window is maximized and on top
- Verify Chrome is the active window (not minimized)
- Try manual shortcut (Right Alt + Shift + P) to test

### "No new tab detected"
- Extension may need more time - increase wait from 15 to 20 seconds
- Verify keyboard shortcut is properly configured
- Try manual shortcut (Alt+Shift+P) to test
- Check Chrome has focus when shortcut is pressed

### Download button not found
- Extension may need more time - increase wait from 15 to 20 seconds
- Check if extension tab actually opened
- Verify extension works manually first (Alt+Shift+P)

### Screenshot not captured
- Make sure page is fully loaded (45 second wait should be enough)
- Check if extension has necessary permissions
- Try manual capture first to verify extension works
- Ensure Chrome window is visible (not minimized)

### Download permission popup not handled
- Script tries multiple methods to detect and click "Allow"
- Check console logs to see which method was used
- If popup still blocks, manually allow downloads for the extension once
- Chrome may remember the permission for future runs

## 🎯 Benefits Over CDP

- ✅ **Professional quality** - Same tool thousands use manually
- ✅ **Handles complex pages** - Better at dealing with dynamic content
- ✅ **Proven reliability** - Well-tested Chrome extension
- ✅ **Better rendering** - Handles modern web apps better
- ✅ **Automatic scrolling** - Smart capture of lazy-loaded content

## 📦 File Structure

```
portoptimizer_screenshot_api/
├── gofullpage.crx              ← Extension file
├── app.py                      ← Flask API
├── automation.py               ← Automation script (loads extension)
├── screenshots/                ← Downloaded screenshots
│   ├── 2024-10-23_15-30-00.png
│   └── ...
└── README.md
```

## 🔄 Alternative: Use CDP Method

If you can't get the extension, you can revert to the CDP method by uncommenting the CDP code in `automation.py`. The extension method is recommended for better quality.

---

**Extension URL**: https://chromewebstore.google.com/detail/gofull-page-full-page-scr/fdpohaocaechififmbbbbbknoalclacl

