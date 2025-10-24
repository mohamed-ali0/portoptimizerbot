from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
from datetime import datetime
import os
import glob
from pynput.keyboard import Controller, Key
import win32gui
import win32con


def bring_chrome_to_front():
    """Force Chrome window to the front and set to fullscreen using aggressive methods"""
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if "Google Chrome" in window_text or "Chrome" in window_text:
                windows.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(callback, windows)
    
    if windows:
        # Get the first Chrome window
        hwnd = windows[0]
        
        # Restore if minimized
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.2)
        
        # Show window normally first
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        time.sleep(0.1)
        
        # Make it topmost temporarily
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        time.sleep(0.1)
        
        # Bring to front
        win32gui.BringWindowToTop(hwnd)
        time.sleep(0.1)
        
        # Set as foreground window
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)
        
        # Remove topmost flag (so other windows can go on top if needed)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
        time.sleep(0.1)
        
        # Maximize
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        
        # Final bring to top
        win32gui.BringWindowToTop(hwnd)
        
        print(f"[{datetime.now()}] Chrome window forcefully brought to front and maximized")
        return True
    return False


def take_screenshot(username, password):
    """
    Automate login to PortOptimizer portal and take a full-page screenshot
    
    Args:
        username: Portal username
        password: Portal password
    
    Returns:
        tuple: (success: bool, message: str)
    """
    driver = None
    
    try:
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use persistent user data directory so extension permissions are remembered
        user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
        os.makedirs(user_data_dir, exist_ok=True)
        chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
        chrome_options.add_argument('--profile-directory=Default')
        print(f"[{datetime.now()}] Using persistent Chrome profile at: {user_data_dir}")
        
        # Load GoFullPage extension
        extension_path = os.path.join(os.getcwd(), "gofullpage.crx")
        if os.path.exists(extension_path):
            chrome_options.add_extension(extension_path)
            print(f"[{datetime.now()}] GoFullPage extension loaded")
        else:
            print(f"[{datetime.now()}] WARNING: gofullpage.crx not found in project directory")
        
        # Set download preferences and grant extension permissions
        download_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(download_dir, exist_ok=True)
        
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            # Auto-grant all permissions for extensions (including downloads)
            "profile.default_content_setting_values.automatic_downloads": 1,
            # Disable extension permission prompts
            "profile.content_settings.exceptions.automatic_downloads": {
                "*,*": {"setting": 1}
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # Add arguments to disable permission prompts
        chrome_options.add_argument('--disable-features=DownloadBubble,DownloadBubbleV2')
        chrome_options.add_argument('--disable-popup-blocking')
        
        # Grant extension permissions at startup
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-service-autorun')
        chrome_options.add_argument('--password-store=basic')
        
        # Uncomment the line below to run in headless mode (without UI)
        # NOTE: GoFullPage extension may not work in headless mode
        # chrome_options.add_argument('--headless=new')
        
        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Maximize window to fullscreen and bring to front
        print(f"[{datetime.now()}] Setting window to fullscreen...")
        driver.maximize_window()
        time.sleep(1)
        
        # Wait for extension to fully initialize
        print(f"[{datetime.now()}] Waiting for extension to initialize...")
        time.sleep(5)
        
        # Check if this is first run - extension permission popup will appear
        # On first run, user must manually click "Allow" for "Manage your downloads" permission
        # After that, it will be remembered in the chrome_profile directory
        print(f"[{datetime.now()}] NOTE: If extension permission popup appears, it will be auto-handled")
        print(f"[{datetime.now()}] If it's the first run, the popup will appear during screenshot download")
        
        # Close any extension welcome/onboarding tabs
        try:
            all_handles = driver.window_handles
            if len(all_handles) > 1:
                print(f"[{datetime.now()}] Closing extension welcome tabs ({len(all_handles)} tabs open)...")
                main_handle = all_handles[0]
                for handle in all_handles[1:]:
                    driver.switch_to.window(handle)
                    driver.close()
                driver.switch_to.window(main_handle)
                print(f"[{datetime.now()}] Extension tabs closed")
        except Exception as e:
            print(f"[{datetime.now()}] Note: {str(e)}")
        
        print(f"[{datetime.now()}] Navigating to portal...")
        
        # Navigate to the portal
        driver.get('https://tower.portoptimizer.com/')
        
        # Wait 30 seconds for page to fully load
        print(f"[{datetime.now()}] Waiting 30s for page to load...")
        time.sleep(30)
        
        # Click the "Log In" button
        print(f"[{datetime.now()}] Clicking login button...")
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.login"))
        )
        login_button.click()
        
        # Wait 30 seconds for login page to load
        print(f"[{datetime.now()}] Waiting 30s for login page...")
        time.sleep(30)
        
        # Enter username
        print(f"[{datetime.now()}] Entering username...")
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='identifier']"))
        )
        username_field.clear()
        username_field.send_keys(username)
        
        # Click "Next" button
        print(f"[{datetime.now()}] Clicking Next button...")
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Next']"))
        )
        next_button.click()
        
        # Wait 15 seconds for password field to appear
        print(f"[{datetime.now()}] Waiting 15s for password field...")
        time.sleep(15)
        
        # Enter password
        print(f"[{datetime.now()}] Entering password...")
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='credentials.passcode']"))
        )
        password_field.clear()
        password_field.send_keys(password)
        
        # Click "Verify" button
        print(f"[{datetime.now()}] Clicking Verify button...")
        verify_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Verify']"))
        )
        verify_button.click()
        
        # Wait 45 seconds for page to fully load
        print(f"[{datetime.now()}] Waiting 45s for page to load after login...")
        time.sleep(45)
        
        # Take full-page screenshot using GoFullPage extension keyboard shortcut
        print(f"[{datetime.now()}] Taking full-page screenshot using GoFullPage extension...")
        
        # Scroll to top first
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(2)
        
        # Store current window handle
        current_window = driver.current_window_handle
        
        # CRITICAL: Force Chrome window to front RIGHT BEFORE triggering extension
        print(f"[{datetime.now()}] Ensuring Chrome window is on top and fullscreen before capture...")
        
        # First attempt - aggressive window forcing
        bring_chrome_to_front()
        time.sleep(1)  # Give it time to settle
        
        # Double-check with Selenium maximize
        driver.maximize_window()
        time.sleep(0.5)
        
        # Force to front again with more time
        print(f"[{datetime.now()}] Second window forcing attempt...")
        bring_chrome_to_front()
        time.sleep(1)  # Longer wait to ensure it's actually on top
        
        # Click on page to ensure focus
        try:
            driver.execute_script("document.body.click();")
        except:
            pass
        time.sleep(0.5)
        
        # Verify window is actually visible and on top
        print(f"[{datetime.now()}] Chrome window should now be visible on top")
        
        # Trigger GoFullPage using keyboard shortcut (Ctrl + Shift + K)
        # NOTE: Alt+Shift+P conflicts with browser "New Tab Group" shortcut
        print(f"[{datetime.now()}] Triggering GoFullPage with keyboard shortcut (Ctrl + Shift + K)...")
        
        # Use pynput to send system-level keyboard events
        # This appears to the OS as real keyboard input
        keyboard = Controller()
        
        # Press and hold Ctrl
        keyboard.press(Key.ctrl)
        time.sleep(0.05)
        
        # Press and hold Shift
        keyboard.press(Key.shift)
        time.sleep(0.1)  # Hold both modifiers for 100ms
        
        # Press K
        keyboard.press('k')
        time.sleep(0.05)
        keyboard.release('k')
        
        # Release modifiers in reverse order
        time.sleep(0.1)
        keyboard.release(Key.shift)
        time.sleep(0.05)
        keyboard.release(Key.ctrl)
        
        print(f"[{datetime.now()}] System keyboard input sent (Ctrl+Shift+K)")
        
        print(f"[{datetime.now()}] Waiting 15 seconds for extension to capture screenshot...")
        time.sleep(15)  # Wait for GoFullPage to capture and open new tab
        
        # Look for the new tab that GoFullPage opened
        print(f"[{datetime.now()}] Looking for extension result tab...")
        all_windows = driver.window_handles
        
        if len(all_windows) > 1:
            # Switch to the new tab (last one opened)
            extension_tab = all_windows[-1]
            driver.switch_to.window(extension_tab)
            print(f"[{datetime.now()}] Found and switched to extension tab ({len(all_windows)} tabs total)")
        else:
            print(f"[{datetime.now()}] WARNING: No new tab detected, extension may not have triggered")
            raise Exception("GoFullPage extension did not open result tab")
        
        # Find and click the download button
        print(f"[{datetime.now()}] Looking for download button...")
        try:
            download_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-download#btn-download"))
            )
            
            # Get the download filename from the button
            download_filename = download_button.get_attribute("download")
            print(f"[{datetime.now()}] Found download button, file: {download_filename}")
            
            # Click download button
            download_button.click()
            print(f"[{datetime.now()}] Download button clicked")
            
            # Wait for potential Chrome extension permission popup
            time.sleep(3)
            
            # Handle Chrome extension permission popup using keyboard (since it's a Chrome system dialog)
            print(f"[{datetime.now()}] Checking for extension permission popup...")
            
            # Try to handle the Chrome extension permission dialog using keyboard navigation
            # Since this is a Chrome system dialog, Selenium can't interact with it
            # We use keyboard: Tab to "Allow" button, then Enter to click it
            keyboard = Controller()
            
            try:
                # Press Tab to focus on "Allow" button (it's usually the default button)
                keyboard.press(Key.tab)
                time.sleep(0.1)
                keyboard.release(Key.tab)
                time.sleep(0.3)
                
                # Press Enter to click "Allow"
                keyboard.press(Key.enter)
                time.sleep(0.1)
                keyboard.release(Key.enter)
                
                print(f"[{datetime.now()}] Attempted to click 'Allow' via keyboard (Tab + Enter)")
                time.sleep(2)  # Wait for permission to be processed
                
            except Exception as e:
                print(f"[{datetime.now()}] No permission popup or already granted: {str(e)}")
            
            # Wait for download to complete
            print(f"[{datetime.now()}] Waiting 10 seconds for download to complete...")
            time.sleep(10)
            
            # Close/kill the extension tab
            print(f"[{datetime.now()}] Closing extension tab...")
            driver.close()
            
            # Switch back to main window
            driver.switch_to.window(current_window)
            print(f"[{datetime.now()}] Switched back to main window")
            
            # Generate our standardized filename
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            final_filename = f"{timestamp}.png"
            screenshots_dir = "screenshots"
            
            # Find the downloaded file and rename it
            downloaded_files = glob.glob(os.path.join(screenshots_dir, "screencapture-*.png"))
            if downloaded_files:
                # Get the most recent file
                latest_file = max(downloaded_files, key=os.path.getctime)
                final_path = os.path.join(screenshots_dir, final_filename)
                
                # Rename to our standard format
                os.rename(latest_file, final_path)
                print(f"[{datetime.now()}] Screenshot saved: {final_filename}")
                return True, final_filename
            else:
                print(f"[{datetime.now()}] WARNING: Downloaded file not found, keeping original name")
                return True, download_filename
                
        except Exception as e:
            print(f"[{datetime.now()}] Error clicking download button: {str(e)}")
            # Switch back to main window
            driver.switch_to.window(current_window)
            raise
    
    except Exception as e:
        error_msg = f"Error taking screenshot: {str(e)}"
        print(f"[{datetime.now()}] {error_msg}")
        return False, error_msg
    
    finally:
        # Close the browser
        if driver:
            try:
                driver.quit()
                print(f"[{datetime.now()}] Browser closed")
            except:
                pass


if __name__ == "__main__":
    # Test the automation
    print("Testing automation script...")
    success, message = take_screenshot("sara@fouroneone.io", "Ss925201!")
    
    if success:
        print(f"✓ Success: {message}")
    else:
        print(f"✗ Failed: {message}")

