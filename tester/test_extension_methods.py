"""
Test all GoFullPage extension triggering methods
Uses the same Chrome profile as the main app
Tests on Google search page
"""
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def test_extension_methods():
    """Test all methods to trigger GoFullPage extension"""
    print("="*80)
    print("GOFULLPAGE EXTENSION TRIGGERING METHODS TEST")
    print("="*80)
    print("Testing different ways to trigger the extension")
    print("Using same Chrome profile as main app")
    print("="*80)
    print()
    
    # Chrome options - same as main app
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    
    # Use the same Chrome profile as main app
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
        
        # Test Method 1: Direct navigation to extension page
        print(f"\n[{datetime.now()}] ===== METHOD 1: Direct Navigation =====")
        try:
            extension_url = "chrome-extension://fdpohaocaechififmbbbbbknoalclacl/capture.html"
            print(f"[{datetime.now()}] Navigating to: {extension_url}")
            driver.get(extension_url)
            time.sleep(5)
            
            current_url = driver.current_url
            print(f"[{datetime.now()}] Current URL: {current_url}")
            
            if "chrome-extension://" in current_url:
                print(f"[{datetime.now()}] ✅ Successfully navigated to extension page")
                
                # Look for download button
                try:
                    download_btn = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "btn-download"))
                    )
                    print(f"[{datetime.now()}] ✅ Found download button!")
                    print(f"[{datetime.now()}] Method 1: SUCCESS")
                except:
                    print(f"[{datetime.now()}] ❌ Download button not found")
                    print(f"[{datetime.now()}] Method 1: FAILED")
            else:
                print(f"[{datetime.now()}] ❌ Not on extension page")
                print(f"[{datetime.now()}] Method 1: FAILED")
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 1 failed: {str(e)}")
            print(f"[{datetime.now()}] Method 1: FAILED")
        
        # Go back to Google for next test
        print(f"\n[{datetime.now()}] Going back to Google...")
        driver.get("https://www.google.com/search?q=cute+puppies")
        time.sleep(3)
        
        # Test Method 2: Open extension in new tab
        print(f"\n[{datetime.now()}] ===== METHOD 2: New Tab =====")
        try:
            print(f"[{datetime.now()}] Opening extension in new tab...")
            driver.execute_script("""
                window.open('chrome-extension://fdpohaocaechififmbbbbbknoalclacl/capture.html', '_blank');
            """)
            
            time.sleep(5)
            print(f"[{datetime.now()}] Number of tabs after opening extension: {len(driver.window_handles)}")
            
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
                
                # Wait for extension to process
                print(f"[{datetime.now()}] Waiting for extension to process...")
                time.sleep(10)
                
                # Look for download button
                try:
                    download_btn = WebDriverWait(driver, 15).until(
                        EC.presence_of_element_located((By.ID, "btn-download"))
                    )
                    print(f"[{datetime.now()}] ✅ Found download button!")
                    print(f"[{datetime.now()}] Method 2: SUCCESS")
                except:
                    print(f"[{datetime.now()}] ❌ Download button not found")
                    print(f"[{datetime.now()}] Method 2: FAILED")
            else:
                print(f"[{datetime.now()}] ❌ Extension tab not found")
                print(f"[{datetime.now()}] Method 2: FAILED")
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 2 failed: {str(e)}")
            print(f"[{datetime.now()}] Method 2: FAILED")
        
        # Go back to Google for next test
        print(f"\n[{datetime.now()}] Going back to Google...")
        driver.get("https://www.google.com/search?q=cute+puppies")
        time.sleep(3)
        
        # Test Method 3: Inject extension script
        print(f"\n[{datetime.now()}] ===== METHOD 3: Script Injection =====")
        try:
            print(f"[{datetime.now()}] Injecting extension script...")
            result = driver.execute_script("""
                // Load and execute the extension's capture logic
                const script = document.createElement('script');
                script.src = 'chrome-extension://fdpohaocaechififmbbbbbknoalclacl/js/page/index.js';
                document.head.appendChild(script);
                
                return 'Script injection attempted';
            """)
            
            print(f"[{datetime.now()}] Script injection result: {result}")
            time.sleep(5)
            
            # Check if new tab opened
            time.sleep(5)
            print(f"[{datetime.now()}] Number of tabs after script injection: {len(driver.window_handles)}")
            
            if len(driver.window_handles) > 1:
                print(f"[{datetime.now()}] ✅ New tab opened!")
                print(f"[{datetime.now()}] Method 3: SUCCESS")
            else:
                print(f"[{datetime.now()}] ❌ No new tab opened")
                print(f"[{datetime.now()}] Method 3: FAILED")
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 3 failed: {str(e)}")
            print(f"[{datetime.now()}] Method 3: FAILED")
        
        # Go back to Google for next test
        print(f"\n[{datetime.now()}] Going back to Google...")
        driver.get("https://www.google.com/search?q=cute+puppies")
        time.sleep(3)
        
        # Test Method 4: CDP Runtime evaluation
        print(f"\n[{datetime.now()}] ===== METHOD 4: CDP Runtime =====")
        try:
            print(f"[{datetime.now()}] Using CDP to trigger extension...")
            result = driver.execute_cdp_cmd("Runtime.evaluate", {
                "expression": """
                    // Try to trigger the extension
                    if (chrome && chrome.runtime) {
                        chrome.runtime.sendMessage('fdpohaocaechififmbbbbbknoalclacl', {
                            action: 'capture'
                        });
                        'Extension message sent via CDP';
                    } else {
                        'Chrome runtime not available';
                    }
                """
            })
            
            print(f"[{datetime.now()}] CDP Result: {result}")
            time.sleep(5)
            
            # Check if new tab opened
            print(f"[{datetime.now()}] Number of tabs after CDP: {len(driver.window_handles)}")
            
            if len(driver.window_handles) > 1:
                print(f"[{datetime.now()}] ✅ New tab opened!")
                print(f"[{datetime.now()}] Method 4: SUCCESS")
            else:
                print(f"[{datetime.now()}] ❌ No new tab opened")
                print(f"[{datetime.now()}] Method 4: FAILED")
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 4 failed: {str(e)}")
            print(f"[{datetime.now()}] Method 4: FAILED")
        
        # Go back to Google for next test
        print(f"\n[{datetime.now()}] Going back to Google...")
        driver.get("https://www.google.com/search?q=cute+puppies")
        time.sleep(3)
        
        # Test Method 5: Extension action trigger
        print(f"\n[{datetime.now()}] ===== METHOD 5: Extension Action =====")
        try:
            print(f"[{datetime.now()}] Triggering extension action...")
            result = driver.execute_cdp_cmd("Runtime.evaluate", {
                "expression": """
                    // Try to trigger the extension action
                    if (chrome && chrome.action) {
                        chrome.action.openPopup();
                        'Extension action triggered';
                    } else {
                        'Chrome action not available';
                    }
                """
            })
            
            print(f"[{datetime.now()}] Action Result: {result}")
            time.sleep(5)
            
            # Check if new tab opened
            print(f"[{datetime.now()}] Number of tabs after action: {len(driver.window_handles)}")
            
            if len(driver.window_handles) > 1:
                print(f"[{datetime.now()}] ✅ New tab opened!")
                print(f"[{datetime.now()}] Method 5: SUCCESS")
            else:
                print(f"[{datetime.now()}] ❌ No new tab opened")
                print(f"[{datetime.now()}] Method 5: FAILED")
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 5 failed: {str(e)}")
            print(f"[{datetime.now()}] Method 5: FAILED")
        
        print(f"\n[{datetime.now()}] All tests completed!")
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Test failed: {str(e)}")
        
    finally:
        if driver:
            print(f"[{datetime.now()}] Closing browser...")
            driver.quit()

if __name__ == "__main__":
    test_extension_methods()
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    print("Check the results above to see which methods worked")
    print("="*80)
    
    input("\nPress Enter to exit...")

