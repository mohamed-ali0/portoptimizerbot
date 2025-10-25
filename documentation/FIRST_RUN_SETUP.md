# First Run Setup Guide

## 🎯 Extension Permission - First Time Only

On the **very first run**, you will see a Chrome extension permission popup:

```
"GoFullPage - Full Page Screen Capture" has requested additional permissions.

It could:
Manage your downloads

[Allow]  [Deny]
```

## ✅ How It's Handled

### Automatic (Keyboard Method)
The automation will **automatically** press `Tab` + `Enter` to click "Allow"

### Persistent Profile
After the first run, the permission is **saved permanently** in the `chrome_profile/` directory

### Future Runs
On all subsequent runs, **no popup will appear** - Chrome remembers the permission!

## 📋 First Run Process

```
1. Extension loads
2. Login to portal
3. Screenshot captured
4. Download button clicked
5. ⚠️ PERMISSION POPUP APPEARS (first time only)
6. Automation presses Tab + Enter to click "Allow"
7. Download proceeds
8. Screenshot saved
```

## 🔄 Subsequent Runs

```
1. Extension loads (uses saved profile)
2. Login to portal  
3. Screenshot captured
4. Download button clicked
5. ✅ NO POPUP (permission already granted)
6. Download proceeds immediately
7. Screenshot saved
```

## 🗂️ Chrome Profile Directory

The automation creates a `chrome_profile/` directory that stores:
- ✅ Extension permissions (including download permission)
- ✅ Extension settings
- ✅ Chrome preferences

**DO NOT DELETE** this directory if you want to avoid the permission popup!

## 🧪 Testing First Run

### Manual Test:
1. Delete `chrome_profile/` directory (if exists)
2. Run: `python app.py`
3. Trigger screenshot: 
   ```bash
   curl -X POST http://localhost:5000/screenshot/now \
     -H "Content-Type: application/json" \
     -d '{"admin_password":"YB02Ss3JJdk"}'
   ```
4. Watch the console - you'll see:
   ```
   [timestamp] Download button clicked
   [timestamp] Checking for extension permission popup...
   [timestamp] Attempted to click 'Allow' via keyboard (Tab + Enter)
   ```
5. Chrome window should show the popup being clicked automatically

### Second Test:
1. Run the same command again
2. No popup should appear!
3. Download should proceed immediately

## ⚙️ How It Works Technically

### Chrome System Dialog Issue
The extension permission popup is a **Chrome system dialog**, not a web page element.
- ❌ Selenium **cannot** interact with Chrome system dialogs
- ❌ DOM selectors **don't work** on system dialogs
- ✅ **Keyboard input works** on system dialogs

### Solution: Keyboard Navigation
```python
keyboard = Controller()

# Focus on "Allow" button
keyboard.press(Key.tab)
keyboard.release(Key.tab)

# Click it
keyboard.press(Key.enter)
keyboard.release(Key.enter)
```

### Persistent Profile
```python
chrome_options.add_argument('--user-data-dir=chrome_profile')
```
This tells Chrome to save all settings/permissions in this directory.

## 🔧 Troubleshooting

### Popup Still Appears Every Time
**Cause**: Chrome profile might be corrupted or locked
**Solution**:
```bash
# Stop Flask app
# Delete the profile
rm -rf chrome_profile/    # Linux/Mac
rmdir /s chrome_profile\  # Windows
# Restart Flask app
```

### "Deny" Gets Clicked Instead
**Cause**: Tab navigation might have changed
**Solution**: Manually click "Allow" on first run, then it will be saved

### Permission Not Saved
**Cause**: Chrome profile directory not writable
**Solution**: Check file permissions on `chrome_profile/` directory

### Chrome Won't Start
**Cause**: Another Chrome instance using the same profile
**Solution**: Close all Chrome windows, then restart Flask app

## 📁 File Structure

```
portoptimizer_screenshot_api/
├── chrome_profile/              ← Created automatically
│   ├── Default/
│   │   ├── Extensions/
│   │   ├── Preferences        ← Extension permissions saved here
│   │   └── ...
│   └── ...
├── gofullpage.crx
├── app.py
└── screenshots/
```

## 🚨 Important Notes

1. **First run takes longer** - Wait for the Tab+Enter automation
2. **Don't delete `chrome_profile/`** - Unless you want to reset everything
3. **One-time setup** - Permission popup only appears once
4. **Automatic after first time** - No manual intervention needed

## ✨ Benefits

- ✅ **One-time manual action** (or fully automatic with keyboard)
- ✅ **Remembered forever** (until you delete chrome_profile/)
- ✅ **No popup on subsequent runs**
- ✅ **Fully automated after first run**

## 🎬 Quick Start

```bash
# First time setup
pip install pynput pywin32
python app.py

# Test first run (permission popup will appear and be auto-handled)
curl -X POST http://localhost:5000/screenshot/now \
  -H "Content-Type: application/json" \
  -d '{"admin_password":"YB02Ss3JJdk"}'

# All future runs - no popup!
```

---

**After the first successful run, the system is fully automated!** 🎉


