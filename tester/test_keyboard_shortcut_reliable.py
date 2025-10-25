"""
Test reliable keyboard shortcut triggering for GoFullPage extension
Focus on making the keyboard shortcut work consistently
"""
import time
import win32api
import win32con
import win32gui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def test_reliable_keyboard_shortcut():
    """Test reliable keyboard shortcut triggering"""
    print("="*80)
    print("RELIABLE KEYBOARD SHORTCUT TEST")
    print("="*80)
    print("Testing different approaches to make keyboard shortcuts work reliably")
    print("="*80)
    print()
    
    # Chrome options - same as main app
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    
    # Use the same Chrome profile as main app
    import os
    chrome_profile_path = os.path.join(os.getcwd(), 'chrome_profile')
    chrome_options.add_argument(f'--user-data-dir={chrome_profile_path}')
    
    # Load the extension
    chrome_options.add_extension('gofullpage.crx')
    
    driver = None
    try:
        print(f"[{datetime.now()}] Starting Chrome with same profile as main app...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to Google
        print(f"[{datetime.now()}] Navigating to Google...")
        driver.get("https://www.google.com")
        time.sleep(3)
        
        # Search for something
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("cute puppies")
        search_box.submit()
        time.sleep(3)
        
        print(f"[{datetime.now()}] On Google search results. Current URL: {driver.current_url}")
        print(f"[{datetime.now()}] Number of tabs: {len(driver.window_handles)}")
        
        # Test Method 1: win32api keyboard events (most reliable)
        print(f"\n[{datetime.now()}] ===== METHOD 1: win32api Keyboard Events =====")
        try:
            print(f"[{datetime.now()}] Sending Alt+Shift+P using win32api...")
            
            # Find Chrome window
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if "Google Chrome" in window_text or "Chrome" in window_text:
                        windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                chrome_hwnd = windows[0]
                print(f"[{datetime.now()}] Found Chrome window, sending Alt+Shift+P...")
                
                # Send Alt+Shift+P using win32api
                # Press and hold Alt
                win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
                time.sleep(0.1)
                
                # Press and hold Shift
                win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
                time.sleep(0.1)
                
                # Press P
                win32api.keybd_event(ord('P'), 0, 0, 0)
                time.sleep(0.1)
                win32api.keybd_event(ord('P'), 0, win32con.KEYEVENTF_KEYUP, 0)
                
                # Release modifiers in reverse order
                time.sleep(0.1)
                win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
                time.sleep(0.1)
                win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
                
                print(f"[{datetime.now()}] Alt+Shift+P sent!")
                
                # Wait for new tab to open
                time.sleep(10)
                
                # Check for new tabs
                all_handles = driver.window_handles
                print(f"[{datetime.now()}] Number of tabs after shortcut: {len(all_handles)}")
                
                if len(all_handles) > 1:
                    print(f"[{datetime.now()}] ✅ New tab opened!")
                    
                    # Check all tabs
                    for i, handle in enumerate(all_handles):
                        driver.switch_to.window(handle)
                        current_url = driver.current_url
                        print(f"[{datetime.now()}] Tab {i+1}: {current_url}")
                        
                        if "chrome-extension://" in current_url and "capture.html" in current_url:
                            print(f"[{datetime.now()}] ✅ Found extension result tab!")
                            
                            # Look for download button
                            try:
                                download_btn = WebDriverWait(driver, 15).until(
                                    EC.presence_of_element_located((By.ID, "btn-download"))
                                )
                                print(f"[{datetime.now()}] ✅ Found download button!")
                                print(f"[{datetime.now()}] Method 1: SUCCESS")
                                return True
                            except:
                                print(f"[{datetime.now()}] ❌ Download button not found")
                                print(f"[{datetime.now()}] Method 1: FAILED")
                else:
                    print(f"[{datetime.now()}] ❌ No new tab opened")
                    print(f"[{datetime.now()}] Method 1: FAILED")
            else:
                print(f"[{datetime.now()}] ❌ Chrome window not found")
                print(f"[{datetime.now()}] Method 1: FAILED")
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 1 failed: {str(e)}")
            print(f"[{datetime.now()}] Method 1: FAILED")
        
        # Test Method 2: Selenium ActionChains
        print(f"\n[{datetime.now()}] ===== METHOD 2: Selenium ActionChains =====")
        try:
            print(f"[{datetime.now()}] Sending Alt+Shift+P using Selenium ActionChains...")
            
            from selenium.webdriver.common.action_chains import ActionChains
            from selenium.webdriver.common.keys import Keys
            
            # Focus on the page
            driver.find_element(By.TAG_NAME, "body").click()
            
            # Send Alt+Shift+P using ActionChains
            actions = ActionChains(driver)
            actions.key_down(Keys.ALT)
            actions.key_down(Keys.SHIFT)
            actions.key_down('P')
            actions.key_up('P')
            actions.key_up(Keys.SHIFT)
            actions.key_up(Keys.ALT)
            actions.perform()
            
            print(f"[{datetime.now()}] Alt+Shift+P sent via ActionChains!")
            
            # Wait for new tab to open
            time.sleep(10)
            
            # Check for new tabs
            all_handles = driver.window_handles
            print(f"[{datetime.now()}] Number of tabs after shortcut: {len(all_handles)}")
            
            if len(all_handles) > 1:
                print(f"[{datetime.now()}] ✅ New tab opened!")
                
                # Check all tabs
                for i, handle in enumerate(all_handles):
                    driver.switch_to.window(handle)
                    current_url = driver.current_url
                    print(f"[{datetime.now()}] Tab {i+1}: {current_url}")
                    
                    if "chrome-extension://" in current_url and "capture.html" in current_url:
                        print(f"[{datetime.now()}] ✅ Found extension result tab!")
                        
                        # Look for download button
                        try:
                            download_btn = WebDriverWait(driver, 15).until(
                                EC.presence_of_element_located((By.ID, "btn-download"))
                            )
                            print(f"[{datetime.now()}] ✅ Found download button!")
                            print(f"[{datetime.now()}] Method 2: SUCCESS")
                            return True
                        except:
                            print(f"[{datetime.now()}] ❌ Download button not found")
                            print(f"[{datetime.now()}] Method 2: FAILED")
            else:
                print(f"[{datetime.now()}] ❌ No new tab opened")
                print(f"[{datetime.now()}] Method 2: FAILED")
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 2 failed: {str(e)}")
            print(f"[{datetime.now()}] Method 2: FAILED")
        
        print(f"\n[{datetime.now()}] All keyboard shortcut methods tested!")
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Test failed: {str(e)}")
        
    finally:
        if driver:
            print(f"[{datetime.now()}] Closing browser...")
            driver.quit()

if __name__ == "__main__":
    success = test_reliable_keyboard_shortcut()
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    if success:
        print("✅ SUCCESS: Found a reliable keyboard shortcut method!")
        print("This can be used in the automation script")
    else:
        print("❌ FAILED: No reliable keyboard shortcut method found")
        print("May need to use Windows Service approach")
    print("="*80)
    
    input("\nPress Enter to exit...")

