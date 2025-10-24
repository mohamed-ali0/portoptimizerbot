# Extension Installation Troubleshooting

## Issue: Extension Fails to Install on Remote Server

### Check 1: Verify Extension File Exists

```bash
# Check if gofullpage.crx exists
cd "C:\Users\Mohamed Ali\Downloads\portoptimizer_screenshot_api"
dir gofullpage.crx
```

If missing, download from:
https://chrome-extension-downloader.com/
Extension URL: https://chromewebstore.google.com/detail/gofull-page-full-page-scr/fdpohaocaechififmbbbbbknoalclacl

### Check 2: View Console Logs

Check the Flask console output when browser starts:
```
[timestamp] GoFullPage extension loaded  ← Should see this
```

OR

```
[timestamp] WARNING: gofullpage.crx not found  ← Extension missing
```

### Check 3: Chrome Extension Blocking

Remote servers often block extension installation. Check Chrome:
1. Open Chrome manually
2. Go to `chrome://extensions/`
3. Enable "Developer mode" (top right)
4. Look for "GoFullPage" extension
5. If not there → extension blocked by policy

### Check 4: Group Policy Blocking

Windows Server might block extensions:
```
1. Press Win+R
2. Type: gpedit.msc
3. Navigate to: Computer Configuration → Administrative Templates → Google → Google Chrome → Extensions
4. Check if "Extension install blocklist" is enabled
```

---

## Solution 1: Manual Extension Installation (Recommended)

Install the extension manually ONCE, then it will persist in the chrome_profile:

### Steps:

1. **Close Flask app** if running

2. **Open Chrome with the profile**:
   ```bash
   cd "C:\Users\Mohamed Ali\Downloads\portoptimizer_screenshot_api"
   start chrome --user-data-dir=chrome_profile --profile-directory=Default
   ```

3. **Install GoFullPage manually**:
   - Go to: https://chromewebstore.google.com/detail/gofull-page-full-page-scr/fdpohaocaechififmbbbbbknoalclacl
   - Click "Add to Chrome"
   - Grant permissions

4. **Set keyboard shortcut**:
   - Go to: `chrome://extensions/shortcuts`
   - Find "GoFullPage"
   - Set shortcut to: **Alt+Shift+P**

5. **Close Chrome**

6. **Start Flask app**:
   ```bash
   python app.py
   ```

Now the extension will be loaded from the chrome_profile automatically!

---

## Solution 2: Use CDP Method (No Extension Required)

If extension installation is blocked, use Chrome DevTools Protocol instead:

### Enable CDP Screenshot in automation.py:

Find this section (around line 320):
```python
# Click download button
download_button.click()
```

Replace the entire screenshot download section with CDP method:

```python
# Use CDP instead of extension
print(f"[{datetime.now()}] Extension not available, using CDP method...")

# Generate filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"{timestamp}.png"
screenshots_dir = "screenshots"
os.makedirs(screenshots_dir, exist_ok=True)
filepath = os.path.join(screenshots_dir, filename)

# Scroll to top
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(2)

# Use CDP to capture full page
result = driver.execute_cdp_cmd("Page.captureScreenshot", {
    "format": "png",
    "captureBeyondViewport": True
})

# Save screenshot
import base64
with open(filepath, "wb") as f:
    f.write(base64.b64decode(result['data']))

print(f"[{datetime.now()}] Screenshot saved: {filename}")
return True, filename
```

---

## Solution 3: Disable Extension Loading

Comment out extension loading to use CDP method:

In `automation.py`, find (around line 91):
```python
# Load GoFullPage extension
extension_path = os.path.join(os.getcwd(), "gofullpage.crx")
if os.path.exists(extension_path):
    chrome_options.add_extension(extension_path)
```

Comment it out:
```python
# Load GoFullPage extension
# DISABLED: Using CDP method instead on remote server
# extension_path = os.path.join(os.getcwd(), "gofullpage.crx")
# if os.path.exists(extension_path):
#     chrome_options.add_extension(extension_path)
print(f"[{datetime.now()}] Using CDP method (no extension)")
```

---

## Check Server Restrictions

### Chrome Extension Policies

Check if extensions are allowed:
```
chrome://policy/
```

Look for:
- `ExtensionInstallBlocklist` - Should not include "*" (all)
- `ExtensionInstallAllowlist` - Should include the extension ID or "*"

### Registry Check (Windows Server)

```powershell
# Check if extensions are blocked
Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Google\Chrome" -Name "ExtensionInstallBlocklist" -ErrorAction SilentlyContinue
```

---

## Recommended Approach for Remote Server

**Best option**: Use **Solution 1** (Manual Installation)

Why:
- ✅ Extension installed once, persists forever
- ✅ Best screenshot quality
- ✅ Handles dynamic content well
- ✅ No code changes needed

If that fails, use **Solution 2** (CDP Method):
- ✅ No extension needed
- ✅ Built into Chrome
- ✅ Good quality
- ⚠️ May not capture some dynamic content

---

## Testing

After applying solution:

```bash
# Test screenshot
curl -X POST http://localhost:5000/screenshot/now \
  -H "Content-Type: application/json" \
  -d "{\"admin_password\":\"YB02Ss3JJdk\"}"
```

Watch console logs for:
- Extension loading (or not)
- Screenshot method being used
- Success/failure messages

