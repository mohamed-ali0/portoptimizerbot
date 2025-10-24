@echo off
echo ========================================
echo Installing Required Packages
echo ========================================
echo.
echo Installing pynput for system-level keyboard automation...
pip install pynput==1.7.6
echo.
echo Installing pywin32 for window management...
pip install pywin32==306
echo.
echo ========================================
echo Packages installed successfully!
echo ========================================
echo.
echo Now make sure to:
echo 1. Place gofullpage.crx in project directory
echo 2. Set keyboard shortcut to Alt+Shift+P in chrome://extensions/shortcuts
echo 3. The script will force Chrome to top and fullscreen automatically
echo.
pause

