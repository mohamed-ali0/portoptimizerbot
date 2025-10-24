# Disable Windows Focus Prevention

## Method 1: Registry Edit (Recommended)

### **Step 1: Open Registry Editor**
```powershell
# Run as Administrator
regedit
```

### **Step 2: Navigate to the Key**
Navigate to:
```
HKEY_CURRENT_USER\Control Panel\Desktop
```

### **Step 3: Create/Modify Values**
Create these DWORD values:

**Value 1:**
- **Name**: `ForegroundLockTimeout`
- **Type**: `DWORD (32-bit)`
- **Value**: `0`

**Value 2:**
- **Name**: `ForegroundFlashCount`
- **Type**: `DWORD (32-bit)`
- **Value**: `0`

### **Step 4: Restart Session**
- Log off and log back in
- OR restart the server

---

## Method 2: PowerShell Commands (Automated)

### **Run as Administrator:**

```powershell
# Disable foreground lock timeout
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "ForegroundLockTimeout" -Value 0 -Type DWord

# Disable foreground flash count
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "ForegroundFlashCount" -Value 0 -Type DWord

# Verify the changes
Get-ItemProperty -Path "HKCU:\Control Panel\Desktop" | Select-Object ForegroundLockTimeout, ForegroundFlashCount
```

**Expected output:**
```
ForegroundLockTimeout : 0
ForegroundFlashCount  : 0
```

---

## Method 3: Batch Script

Create a file `disable_focus_block.bat`:

```batch
@echo off
echo Disabling Windows focus prevention...

reg add "HKCU\Control Panel\Desktop" /v ForegroundLockTimeout /t REG_DWORD /d 0 /f
reg add "HKCU\Control Panel\Desktop" /v ForegroundFlashCount /t REG_DWORD /d 0 /f

echo.
echo Changes applied! Please log off and log back in.
echo.
pause
```

**Run as Administrator:**
```cmd
disable_focus_block.bat
```

---

## Method 4: Group Policy (Windows Server)

If you have Group Policy access:

1. Open **Group Policy Management Console**
2. Navigate to: **User Configuration → Administrative Templates → Control Panel → Desktop**
3. Find: **"Foreground lock timeout"**
4. Set to: **Enabled** with value **0**
5. Apply and restart

---

## Verification

After applying any method:

### **Test 1: Check Registry**
```powershell
Get-ItemProperty -Path "HKCU:\Control Panel\Desktop" | Select-Object ForegroundLockTimeout, ForegroundFlashCount
```

### **Test 2: Test Your App**
```powershell
# Restart Flask
python app.py

# Test screenshot
curl -X POST http://localhost:5000/screenshot/now `
  -H "Content-Type: application/json" `
  -d '{\"admin_password\":\"YB02Ss3JJdk\"}'
```

**Expected result:**
- No more `SetForegroundWindow` errors
- Chrome window comes to front
- Screenshot completes successfully

---

## Troubleshooting

### **If PowerShell command fails:**
```powershell
# Check if you're running as Administrator
whoami /groups | findstr "S-1-5-32-544"

# If not, run PowerShell as Administrator
```

### **If registry edit fails:**
1. Make sure you're logged in as the user who runs the Flask app
2. Try the manual registry editor method
3. Check if Group Policy is overriding the setting

### **If it still doesn't work:**
1. **Restart the server** (not just log off/on)
2. **Check Windows version** - some versions have additional restrictions
3. **Try running Chrome with different flags:**

```python
# In automation.py, add these Chrome options:
chrome_options.add_argument('--disable-features=TranslateUI')
chrome_options.add_argument('--disable-ipc-flooding-protection')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
```

---

## Alternative: Remove Window Management

If you can't disable the restriction, just remove window management:

```python
# Comment out this line in automation.py:
# bring_chrome_to_front()
```

The automation will still work, just without visible window management.

---

## Security Note

⚠️ **Disabling focus prevention reduces security:**
- Any program can steal focus
- Malicious software could hijack your session
- Only do this on servers you fully control

**For production servers, consider:**
- Running the app as a service with specific permissions
- Using a dedicated user account for automation
- Implementing proper access controls
