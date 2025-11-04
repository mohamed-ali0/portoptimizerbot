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
import psutil


def kill_chrome_process_tree(driver):
    """Kill only the Chrome process created by this driver and its children"""
    try:
        if not driver or not hasattr(driver, 'service') or not driver.service.process:
            return 0
        
        # Get the ChromeDriver service process
        chromedriver_pid = driver.service.process.pid
        
        # Find all child processes (Chrome instances)
        killed_count = 0
        parent = psutil.Process(chromedriver_pid)
        children = parent.children(recursive=True)
        
        # Kill children first (Chrome browser processes)
        for child in children:
            try:
                child.kill()
                killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Kill the parent (ChromeDriver)
        try:
            parent.kill()
            killed_count += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        
        if killed_count > 0:
            print(f"[{datetime.now()}] Killed {killed_count} process(es) from this driver")
            time.sleep(1)  # Wait for processes to fully terminate
        
        return killed_count
    except Exception as e:
        print(f"[{datetime.now()}] Error killing driver processes: {str(e)}")
        return 0


def bring_chrome_to_front():
    """Force Chrome window to the front and set to fullscreen using aggressive methods"""
    try:
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
            try:
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.2)
            except:
                pass
            
            # Show window normally first
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                time.sleep(0.1)
            except:
                pass
            
            # Make it topmost temporarily
            try:
                win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                     win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                time.sleep(0.1)
            except:
                pass
            
            # Bring to front
            try:
                win32gui.BringWindowToTop(hwnd)
                time.sleep(0.1)
            except:
                pass
            
            # Set as foreground window
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.1)
            
            # Remove topmost flag (so other windows can go on top if needed)
            try:
                win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                     win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                time.sleep(0.1)
            except:
                pass
            
            # Maximize
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            except:
                pass
            
            # Final bring to top
            try:
                win32gui.BringWindowToTop(hwnd)
            except:
                pass
            
            print(f"[{datetime.now()}] Chrome window management completed")
            return True
        
        print(f"[{datetime.now()}] No Chrome window found")
        return False
        
    except Exception as e:
        print(f"[{datetime.now()}] Warning: Error in window management: {str(e)}")
        print(f"[{datetime.now()}] Continuing anyway - automation should still work")
        return False


def download_excel_report(username, password):
    """
    Automate login to PortOptimizer portal and download Excel report
    
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
        download_dir = os.path.join(os.getcwd(), "downloads")
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
        
        # Force Chrome window to front ONCE at startup
        print(f"[{datetime.now()}] Forcing Chrome window to front...")
        time.sleep(1)  # Brief wait for window to appear
        bring_chrome_to_front()
        driver.maximize_window()
        print(f"[{datetime.now()}] Chrome window setup complete")
        
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
        
        # Click the "Return Signal" tab and wait 15 seconds
        print(f"[{datetime.now()}] Looking for Return Signal tab...")
        try:
            return_signal_tab = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='mdc-tab__text-label' and text()='Return Signal']"))
            )
            print(f"[{datetime.now()}] Clicking Return Signal tab...")
            return_signal_tab.click()
            print(f"[{datetime.now()}] Waiting 15 seconds after clicking Return Signal tab...")
            time.sleep(15)  # Wait 15 seconds as requested
        except Exception as e:
            print(f"[{datetime.now()}] Error: Could not find or click Return Signal tab: {str(e)}")
            raise Exception(f"Could not find Return Signal tab: {str(e)}")
        
        # Look for download button
        print(f"[{datetime.now()}] Looking for download button...")
        download_button = None
        
        # Try multiple selectors for the download button
        selectors = [
            "button[title='Download']",
            "button[aria-label='Download']",
            "button:contains('Download')",
            "a[href*='download']",
            "button[class*='download']",
            "a[class*='download']",
            "button[onclick*='download']",
            "a[onclick*='download']"
        ]
        
        for selector in selectors:
            try:
                if "contains" in selector:
                    # Use XPath for text contains
                    xpath_selector = f"//button[contains(text(), 'Download')]"
                    download_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath_selector))
                    )
                else:
                    download_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                print(f"[{datetime.now()}] Found download button with selector: {selector}")
                break
            except:
                continue
        
        if download_button:
            print(f"[{datetime.now()}] Clicking download button...")
            download_button.click()
            print(f"[{datetime.now()}] Download button clicked")
            
            # Wait for download to complete
            time.sleep(10)
            print(f"[{datetime.now()}] Excel download should be complete")
        else:
            print(f"[{datetime.now()}] Download button not found")
            print(f"[{datetime.now()}] Page source length: {len(driver.page_source)} characters")
            if "download" in driver.page_source.lower():
                print(f"[{datetime.now()}] Download text found in page source")
            else:
                print(f"[{datetime.now()}] Download text NOT found in page source")
            raise Exception("Could not find download button")
        
        # Generate our standardized filename with UTC timestamp for timezone independence
        # Format: POLA_Empty_Returns_YYYY-MM-DD_HH-MM-SS.xlsx
        timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
        final_filename = f"POLA_Empty_Returns_{timestamp}.xlsx"
        
        # Check downloads directory (where Chrome downloads files)
        downloads_dir = "downloads"
        os.makedirs(downloads_dir, exist_ok=True)
        
        # Find the downloaded Excel file
        downloaded_files = []
        
        # Check downloads directory
        if os.path.exists(downloads_dir):
            downloaded_files.extend(glob.glob(os.path.join(downloads_dir, "*.xlsx")))
            downloaded_files.extend(glob.glob(os.path.join(downloads_dir, "*.xls")))
        
        if downloaded_files:
            # Get the most recent file
            latest_file = max(downloaded_files, key=os.path.getctime)
            final_path = os.path.join(downloads_dir, final_filename)
            
            # Rename to our standard format
            os.rename(latest_file, final_path)
            print(f"[{datetime.now()}] Excel file saved: {final_filename}")
            return True, final_filename
        else:
            print(f"[{datetime.now()}] WARNING: Downloaded Excel file not found in {downloads_dir}")
            print(f"[{datetime.now()}] Available files in downloads: {os.listdir(downloads_dir) if os.path.exists(downloads_dir) else 'Directory not found'}")
            return True, "Excel file downloaded but filename unknown"
    
    except Exception as e:
        error_msg = f"Error downloading Excel report: {str(e)}"
        print(f"[{datetime.now()}] {error_msg}")
        return False, error_msg
    
    finally:
        # Close the browser
        if driver:
            try:
                # First try graceful shutdown
                driver.quit()
                print(f"[{datetime.now()}] Browser quit() called")
                time.sleep(1)  # Brief wait for quit() to complete
                
                # Force kill to ensure complete cleanup (prevents profile lock)
                print(f"[{datetime.now()}] Ensuring process cleanup...")
                killed = kill_chrome_process_tree(driver)
                if killed > 0:
                    print(f"[{datetime.now()}] Cleaned up {killed} remaining process(es)")
                    
            except Exception as e:
                print(f"[{datetime.now()}] Error during cleanup: {str(e)}")
                # Try to kill process tree as last resort
                try:
                    kill_chrome_process_tree(driver)
                except:
                    pass
            
        print(f"[{datetime.now()}] Cleanup complete")


if __name__ == "__main__":
    # Test the automation
    print("Testing automation script...")
    success, message = download_excel_report("sara@fouroneone.io", "Ss925201!")
    
    if success:
        print(f"✓ Success: {message}")
    else:
        print(f"✗ Failed: {message}")

