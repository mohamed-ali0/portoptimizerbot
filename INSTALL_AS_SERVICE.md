# Install Flask App as Windows Service

## Step 1: Download NSSM

### **Download NSSM:**
1. Go to: https://nssm.cc/download
2. Download: **nssm 2.24** (or latest version)
3. Extract the ZIP file
4. Copy `nssm.exe` to your server (e.g., `C:\nssm\`)

### **Or use PowerShell:**
```powershell
# Create directory
mkdir C:\nssm

# Download NSSM
Invoke-WebRequest -Uri "https://nssm.cc/release/nssm-2.24.zip" -OutFile "C:\nssm\nssm.zip"

# Extract
Expand-Archive -Path "C:\nssm\nssm.zip" -DestinationPath "C:\nssm" -Force
```

---

## Step 2: Create Service Wrapper Script

### **Create `run_service.py` in your project directory:**

```python
import os
import sys
import subprocess
from pathlib import Path

# Get the directory where this script is located
project_dir = Path(__file__).parent.absolute()
os.chdir(project_dir)

# Set environment variables
os.environ['PYTHONPATH'] = str(project_dir)
os.environ['FLASK_APP'] = 'app.py'

# Run the Flask app
if __name__ == "__main__":
    try:
        # Start Flask app
        subprocess.run([sys.executable, "app.py"], cwd=project_dir)
    except KeyboardInterrupt:
        print("Service stopped")
    except Exception as e:
        print(f"Service error: {e}")
        sys.exit(1)
```

### **Create `start_service.bat`:**

```batch
@echo off
cd /d "C:\Users\Administrator\Downloads\portoptimizerbot"
python app.py
```

---

## Step 3: Install as Service

### **Run PowerShell as Administrator:**

```powershell
# Navigate to NSSM directory
cd C:\nssm

# Install the service
.\nssm.exe install "PortOptimizerScreenshot" "C:\Users\Administrator\Downloads\portoptimizerbot\start_service.bat"

# Set service description
.\nssm.exe set "PortOptimizerScreenshot" Description "PortOptimizer Screenshot API Service"

# Set working directory
.\nssm.exe set "PortOptimizerScreenshot" AppDirectory "C:\Users\Administrator\Downloads\portoptimizerbot"

# Set startup type to Automatic
.\nssm.exe set "PortOptimizerScreenshot" Start SERVICE_AUTO_START

# Set service to restart on failure
.\nssm.exe set "PortOptimizerScreenshot" AppExit Default Restart

# Set restart delay (5 seconds)
.\nssm.exe set "PortOptimizerScreenshot" AppRestartDelay 5000

# Set service to run as SYSTEM (for keyboard access)
.\nssm.exe set "PortOptimizerScreenshot" ObjectName LocalSystem

# Allow service to interact with desktop (for Chrome)
.\nssm.exe set "PortOptimizerScreenshot" Type SERVICE_INTERACTIVE_PROCESS
```

---

## Step 4: Start the Service

```powershell
# Start the service
.\nssm.exe start "PortOptimizerScreenshot"

# Check service status
.\nssm.exe status "PortOptimizerScreenshot"

# View service logs
.\nssm.exe show "PortOptimizerScreenshot"
```

---

## Step 5: Service Management Commands

### **Start/Stop/Restart:**
```powershell
# Start service
net start PortOptimizerScreenshot

# Stop service  
net stop PortOptimizerScreenshot

# Restart service
net stop PortOptimizerScreenshot
net start PortOptimizerScreenshot
```

### **Check Status:**
```powershell
# Check if running
sc query PortOptimizerScreenshot

# View service details
.\nssm.exe show "PortOptimizerScreenshot"
```

### **View Logs:**
```powershell
# View service output
.\nssm.exe show "PortOptimizerScreenshot" AppStdout
.\nssm.exe show "PortOptimizerScreenshot" AppStderr
```

---

## Step 6: Configure Service Properties

### **Set Service to Auto-Start:**
```powershell
# Set to automatic startup
sc config PortOptimizerScreenshot start= auto

# Set to start with system
sc config PortOptimizerScreenshot start= auto
```

### **Set Recovery Options:**
```powershell
# Restart on failure
sc failure PortOptimizerScreenshot reset= 86400 actions= restart/5000/restart/5000/restart/5000
```

---

## Step 7: Test the Service

### **Test API Endpoints:**
```powershell
# Test if service is running
curl http://localhost:5000/status

# Test screenshot
curl -X POST http://localhost:5000/screenshot/now `
  -H "Content-Type: application/json" `
  -d '{\"admin_password\":\"YB02Ss3JJdk\"}'
```

---

## Troubleshooting

### **If Service Won't Start:**

1. **Check logs:**
   ```powershell
   .\nssm.exe show "PortOptimizerScreenshot" AppStdout
   .\nssm.exe show "PortOptimizerScreenshot" AppStderr
   ```

2. **Test manually:**
   ```powershell
   cd "C:\Users\Administrator\Downloads\portoptimizerbot"
   python app.py
   ```

3. **Check permissions:**
   ```powershell
   # Make sure service has access to files
   icacls "C:\Users\Administrator\Downloads\portoptimizerbot" /grant "NT AUTHORITY\SYSTEM:(OI)(CI)F"
   ```

### **If Chrome Won't Start:**

1. **Allow service to interact with desktop:**
   ```powershell
   .\nssm.exe set "PortOptimizerScreenshot" Type SERVICE_INTERACTIVE_PROCESS
   ```

2. **Set Chrome to run in service mode:**
   ```python
   # In automation.py, add these Chrome options:
   chrome_options.add_argument('--no-sandbox')
   chrome_options.add_argument('--disable-dev-shm-usage')
   chrome_options.add_argument('--disable-gpu')
   chrome_options.add_argument('--remote-debugging-port=9222')
   ```

### **If Keyboard Shortcuts Don't Work:**

1. **Run as LocalSystem (already set above)**
2. **Enable interactive services:**
   ```powershell
   # Edit registry
   reg add "HKLM\SYSTEM\CurrentControlSet\Control\Windows" /v NoInteractiveServices /t REG_DWORD /d 0 /f
   ```

---

## Uninstall Service

```powershell
# Stop service
net stop PortOptimizerScreenshot

# Remove service
.\nssm.exe remove "PortOptimizerScreenshot" confirm
```

---

## Benefits of Running as Service

✅ **Runs independently** of user sessions
✅ **Starts automatically** on server boot
✅ **Survives RDP disconnections**
✅ **Runs in background** without visible windows
✅ **Automatic restart** on failure
✅ **System-level permissions** for Chrome automation

---

## Quick Setup Script

Create `install_service.ps1`:

```powershell
# Run as Administrator
$projectPath = "C:\Users\Administrator\Downloads\portoptimizerbot"
$nssmPath = "C:\nssm\nssm.exe"

# Install service
& $nssmPath install "PortOptimizerScreenshot" "$projectPath\start_service.bat"
& $nssmPath set "PortOptimizerScreenshot" AppDirectory $projectPath
& $nssmPath set "PortOptimizerScreenshot" Start SERVICE_AUTO_START
& $nssmPath set "PortOptimizerScreenshot" ObjectName LocalSystem
& $nssmPath set "PortOptimizerScreenshot" Type SERVICE_INTERACTIVE_PROCESS

# Start service
& $nssmPath start "PortOptimizerScreenshot"

Write-Host "Service installed and started!"
```

**Run as Administrator:**
```powershell
.\install_service.ps1
```
