# Enable Background Keyboard Input on Windows

## Method 1: Disable RDP Session Timeout (Recommended)

### **Registry Modifications:**

```powershell
# Run as Administrator

# Disable session timeout completely
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v KeepAliveEnable /t REG_DWORD /d 1 /f

# Disable idle timeout
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxIdleTime /t REG_DWORD /d 0 /f

# Disable disconnect timeout
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxDisconnectionTime /t REG_DWORD /d 0 /f

# Keep session alive when minimized
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v KeepAliveInterval /t REG_DWORD /d 1 /f
```

---

## Method 2: Enable Interactive Services

### **Allow Services to Interact with Desktop:**

```powershell
# Run as Administrator

# Enable interactive services
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Windows" /v NoInteractiveServices /t REG_DWORD /d 0 /f

# Allow services to interact with desktop
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v ProtectionMode /t REG_DWORD /d 0 /f
```

---

## Method 3: Disable Windows Focus Prevention

### **Disable Foreground Window Restrictions:**

```powershell
# Run as Administrator

# Disable foreground lock timeout
reg add "HKCU\Control Panel\Desktop" /v ForegroundLockTimeout /t REG_DWORD /d 0 /f

# Disable foreground flash count
reg add "HKCU\Control Panel\Desktop" /v ForegroundFlashCount /t REG_DWORD /d 0 /f

# Allow background processes to set foreground
reg add "HKCU\Control Panel\Desktop" /v HungAppTimeout /t REG_DWORD /d 5000 /f
```

---

## Method 4: RDP Session Configuration

### **Configure RDP to Maintain Active Sessions:**

```powershell
# Run as Administrator

# Set RDP to keep sessions active
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fSingleSessionPerUser /t REG_DWORD /d 0 /f

# Disable session disconnection
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v fDisableAutoReconnect /t REG_DWORD /d 0 /f

# Enable session persistence
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v fInheritAutoLogon /t REG_DWORD /d 1 /f
```

---

## Method 5: Windows Input System Modifications

### **Enable Background Input Processing:**

```powershell
# Run as Administrator

# Allow background input
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f

# Disable input filtering
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4D36E96C-E325-11CE-BFC1-08002BE10318}" /v UpperFilters /t REG_SZ /d "" /f

# Enable raw input
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4D36E96C-E325-11CE-BFC1-08002BE10318}" /v LowerFilters /t REG_SZ /d "" /f
```

---

## Method 6: Complete Automation Setup

### **All-in-One Registry Script:**

Create `enable_background_keyboard.reg`:

```registry
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server]
"KeepAliveEnable"=dword:00000001
"fSingleSessionPerUser"=dword:00000000

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp]
"MaxIdleTime"=dword:00000000
"MaxDisconnectionTime"=dword:00000000
"KeepAliveInterval"=dword:00000001
"fDisableAutoReconnect"=dword:00000000
"fInheritAutoLogon"=dword:00000001

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Windows]
"NoInteractiveServices"=dword:00000000

[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager]
"ProtectionMode"=dword:00000000

[HKEY_CURRENT_USER\Control Panel\Desktop]
"ForegroundLockTimeout"=dword:00000000
"ForegroundFlashCount"=dword:00000000
"HungAppTimeout"=dword:00001388

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System]
"EnableLUA"=dword:00000000
```

**Apply by double-clicking the .reg file**

---

## Method 7: PowerShell All-in-One Script

Create `enable_background_keyboard.ps1`:

```powershell
# Run as Administrator
Write-Host "Enabling background keyboard input..."

# RDP Session Configuration
Write-Host "Configuring RDP sessions..."
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v KeepAliveEnable /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fSingleSessionPerUser /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxIdleTime /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v MaxDisconnectionTime /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v KeepAliveInterval /t REG_DWORD /d 1 /f

# Interactive Services
Write-Host "Enabling interactive services..."
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Windows" /v NoInteractiveServices /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager" /v ProtectionMode /t REG_DWORD /d 0 /f

# Focus Prevention
Write-Host "Disabling focus prevention..."
reg add "HKCU\Control Panel\Desktop" /v ForegroundLockTimeout /t REG_DWORD /d 0 /f
reg add "HKCU\Control Panel\Desktop" /v ForegroundFlashCount /t REG_DWORD /d 0 /f
reg add "HKCU\Control Panel\Desktop" /v HungAppTimeout /t REG_DWORD /d 5000 /f

# Input System
Write-Host "Configuring input system..."
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f

Write-Host "Configuration complete!"
Write-Host "Please restart the server for all changes to take effect."
```

---

## Method 8: Group Policy (Windows Server)

### **If you have Group Policy access:**

1. **Open Group Policy Management Console**
2. **Navigate to:** Computer Configuration → Administrative Templates → Windows Components → Remote Desktop Services
3. **Configure these policies:**
   - **"Set time limit for active Remote Desktop Services sessions"** → **Disabled**
   - **"Set time limit for disconnected Remote Desktop Services sessions"** → **Disabled**
   - **"Allow users to connect remotely by using Remote Desktop Services"** → **Enabled**

---

## Verification

### **After applying changes:**

1. **Restart the server**
2. **Test your automation:**
   ```powershell
   # Minimize RDP window
   # Run your Flask app
   python app.py
   
   # Test from another machine
   curl -X POST http://YOUR_SERVER_IP:5000/screenshot/now `
     -H "Content-Type: application/json" `
     -d '{\"admin_password\":\"YB02Ss3JJdk\"}'
   ```

### **Check if changes worked:**
```powershell
# Check RDP settings
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp"

# Check focus settings
reg query "HKCU\Control Panel\Desktop"
```

---

## Troubleshooting

### **If keyboard still doesn't work:**

1. **Check Windows version** - Some restrictions are version-specific
2. **Try Method 7** (PowerShell script) - Most comprehensive
3. **Restart server** after applying changes
4. **Check if antivirus** is blocking registry changes
5. **Verify user permissions** - Some changes require specific rights

### **Alternative: Use VNC instead of RDP**
- VNC maintains active sessions better than RDP
- Install TightVNC or UltraVNC
- VNC doesn't have the same session restrictions

---

## Security Note

⚠️ **These changes reduce security:**
- Disables session timeouts
- Allows background input processing
- Reduces Windows security restrictions

**Only apply on servers you fully control!**

---

## Quick Test

**After applying changes:**
1. **Restart server**
2. **Minimize RDP window**
3. **Run your Flask app**
4. **Test screenshot** - should work even with minimized RDP!

**Method 7 (PowerShell script) is the most comprehensive solution!** 🎯

