"""
Test direct GoFullPage extension triggering methods
This bypasses keyboard shortcuts and triggers the extension directly
"""
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def test_direct_extension_trigger():
    """Test different ways to trigger GoFullPage extension directly"""
    print("="*80)
    print("DIRECT GOFULLPAGE EXTENSION TRIGGER TEST")
    print("="*80)
    print("This will test different methods to trigger the extension")
    print("without using keyboard shortcuts")
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
        
        # Navigate to a test page
        test_url = "https://tower.portoptimizer.com/"
        print(f"[{datetime.now()}] Navigating to: {test_url}")
        driver.get(test_url)
        time.sleep(5)  # Wait for page to load
        
        print(f"[{datetime.now()}] Testing direct extension trigger methods...")
        
        # Method 1: Direct navigation to extension capture page
        print(f"[{datetime.now()}] Method 1: Direct navigation to extension capture page")
        try:
            extension_url = "chrome-extension://fdpohaocaechififmbbbbbknoalclacl/capture.html"
            driver.get(extension_url)
            time.sleep(3)
            
            # Check if we're on the extension page
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
                    return True
                except:
                    print(f"[{datetime.now()}] ❌ Download button not found")
            else:
                print(f"[{datetime.now()}] ❌ Not on extension page")
                
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 1 failed: {str(e)}")
        
        # Method 2: CDP Runtime evaluation
        print(f"[{datetime.now()}] Method 2: CDP Runtime evaluation")
        try:
            # Go back to the test page
            driver.get(test_url)
            time.sleep(3)
            
            # Use CDP to trigger extension
            result = driver.execute_cdp_cmd("Runtime.evaluate", {
                "expression": """
                    if (chrome && chrome.runtime) {
                        chrome.runtime.sendMessage('fdpohaocaechififmbbbbbknoalclacl', {
                            action: 'capture'
                        });
                        'Extension message sent';
                    } else {
                        'Chrome runtime not available';
                    }
                """
            })
            print(f"[{datetime.now()}] CDP Result: {result}")
            
            # Wait for new tab to open
            time.sleep(5)
            
            # Check for new tabs
            all_handles = driver.window_handles
            print(f"[{datetime.now()}] Window handles: {len(all_handles)}")
            
            for handle in all_handles:
                driver.switch_to.window(handle)
                current_url = driver.current_url
                print(f"[{datetime.now()}] Tab URL: {current_url}")
                
                if "chrome-extension://" in current_url and "capture.html" in current_url:
                    print(f"[{datetime.now()}] ✅ Found extension result tab!")
                    
                    # Look for download button
                    try:
                        download_btn = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "btn-download"))
                        )
                        print(f"[{datetime.now()}] ✅ Found download button!")
                        return True
                    except:
                        print(f"[{datetime.now()}] ❌ Download button not found")
                        
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 2 failed: {str(e)}")
        
        # Method 3: JavaScript execution
        print(f"[{datetime.now()}] Method 3: JavaScript execution")
        try:
            # Go back to the test page
            driver.get(test_url)
            time.sleep(3)
            
            # Execute JavaScript to trigger extension
            result = driver.execute_script("""
                // Try to trigger the extension
                if (typeof chrome !== 'undefined' && chrome.runtime) {
                    chrome.runtime.sendMessage('fdpohaocaechififmbbbbbknoalclacl', {
                        action: 'capture',
                        tabId: arguments[0]
                    });
                    return 'Extension triggered via JavaScript';
                } else {
                    return 'Chrome runtime not available';
                }
            """, driver.current_window_handle)
            
            print(f"[{datetime.now()}] JavaScript Result: {result}")
            
            # Wait for new tab to open
            time.sleep(5)
            
            # Check for new tabs
            all_handles = driver.window_handles
            print(f"[{datetime.now()}] Window handles: {len(all_handles)}")
            
            for handle in all_handles:
                driver.switch_to.window(handle)
                current_url = driver.current_url
                print(f"[{datetime.now()}] Tab URL: {current_url}")
                
                if "chrome-extension://" in current_url and "capture.html" in current_url:
                    print(f"[{datetime.now()}] ✅ Found extension result tab!")
                    
                    # Look for download button
                    try:
                        download_btn = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "btn-download"))
                        )
                        print(f"[{datetime.now()}] ✅ Found download button!")
                        return True
                    except:
                        print(f"[{datetime.now()}] ❌ Download button not found")
                        
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Method 3 failed: {str(e)}")
        
        print(f"[{datetime.now()}] ❌ All methods failed")
        return False
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Test failed: {str(e)}")
        return False
        
    finally:
        if driver:
            print(f"[{datetime.now()}] Closing browser...")
            driver.quit()

if __name__ == "__main__":
    success = test_direct_extension_trigger()
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    if success:
        print("✅ SUCCESS: Found a way to trigger the extension directly!")
        print("This can be used in the automation script instead of keyboard shortcuts")
    else:
        print("❌ FAILED: No direct trigger method worked")
        print("Keyboard shortcuts may still be the only reliable method")
    print("="*80)
    
    input("\nPress Enter to exit...")

