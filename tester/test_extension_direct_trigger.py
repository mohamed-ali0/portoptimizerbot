"""
Test direct GoFullPage extension triggering while staying on the same page
This opens the extension in a new tab without leaving the portal page
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def test_extension_while_staying_on_page():
    """Test triggering extension while staying on the portal page"""
    print("="*80)
    print("GOFULLPAGE EXTENSION - STAY ON SAME PAGE TEST")
    print("="*80)
    print("This will trigger the extension while keeping the portal page active")
    print("="*80)
    print()
    
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    
    # Load the extension
    chrome_options.add_extension('gofullpage.crx')
    
    driver = None
    try:
        print(f"[{datetime.now()}] Starting Chrome with GoFullPage extension...")
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to the portal page
        portal_url = "https://tower.portoptimizer.com/"
        print(f"[{datetime.now()}] Navigating to portal: {portal_url}")
        driver.get(portal_url)
        time.sleep(5)  # Wait for page to load
        
        print(f"[{datetime.now()}] Portal page loaded. Current URL: {driver.current_url}")
        print(f"[{datetime.now()}] Number of tabs: {len(driver.window_handles)}")
        
        # Method 1: Open extension in new tab while staying on portal page
        print(f"[{datetime.now()}] Method 1: Opening extension in new tab...")
        try:
            # Open extension capture page in new tab
            driver.execute_script("""
                window.open('chrome-extension://fdpohaocaechififmbbbbbknoalclacl/capture.html', '_blank');
            """)
            
            # Wait for new tab to open
            time.sleep(3)
            
            print(f"[{datetime.now()}] After opening extension. Number of tabs: {len(driver.window_handles)}")
            
            # Check all tabs
            all_handles = driver.window_handles
            extension_tab = None
            
            for i, handle in enumerate(all_handles):
                driver.switch_to.window(handle)
                current_url = driver.current_url
                print(f"[{datetime.now()}] Tab {i+1}: {current_url}")
                
                if "chrome-extension://" in current_url and "capture.html" in current_url:
                    extension_tab = handle
                    print(f"[{datetime.now()}] ✅ Found extension result tab!")
                    break
            
            if extension_tab:
                # Switch to extension tab
                driver.switch_to.window(extension_tab)
                print(f"[{datetime.now()}] Switched to extension tab")
                
                # Wait for extension to process and look for download button
                print(f"[{datetime.now()}] Waiting for extension to process...")
                time.sleep(10)  # Give extension time to capture
                
                # Look for download button
                try:
                    download_btn = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, "btn-download"))
                    )
                    print(f"[{datetime.now()}] ✅ Found download button!")
                    
                    # Click download button
                    download_btn.click()
                    print(f"[{datetime.now()}] ✅ Clicked download button!")
                    
                    # Switch back to portal page
                    for handle in all_handles:
                        driver.switch_to.window(handle)
                        if "tower.portoptimizer.com" in driver.current_url:
                            print(f"[{datetime.now()}] ✅ Back on portal page: {driver.current_url}")
                            break
                    
                    return True
                    
                except Exception as e:
                    print(f"[{datetime.now()}] ❌ Download button not found: {str(e)}")
                    
                    # Check page source for clues
                    page_source = driver.page_source
                    if "btn-download" in page_source:
                        print(f"[{datetime.now()}] Download button exists in source but not clickable")
                    else:
                        print(f"[{datetime.now()}] Download button not in page source")
                    
                    return False
            else:
                print(f"[{datetime.now()}] ❌ Extension tab not found")
                return False
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 1 failed: {str(e)}")
            return False
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Test failed: {str(e)}")
        return False
        
    finally:
        if driver:
            print(f"[{datetime.now()}] Closing browser...")
            driver.quit()

if __name__ == "__main__":
    success = test_extension_while_staying_on_page()
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    if success:
        print("✅ SUCCESS: Extension triggered while staying on portal page!")
        print("This method can be used in the automation script")
    else:
        print("❌ FAILED: Extension trigger method didn't work")
    print("="*80)
    
    input("\nPress Enter to exit...")

