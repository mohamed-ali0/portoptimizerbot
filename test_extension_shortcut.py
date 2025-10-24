"""
Test script to verify GoFullPage extension keyboard shortcut works
Run this script to test Ctrl+Shift+K triggering the extension
"""
import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pynput.keyboard import Controller, Key

def test_extension_shortcut():
    """Test that the extension keyboard shortcut works"""
    print("="*80)
    print("GoFullPage Extension Keyboard Shortcut Test")
    print("="*80)
    
    # Check profile exists
    profile_dir = os.path.join(os.getcwd(), "chrome_profile")
    if not os.path.exists(profile_dir):
        print("\n[ERROR] chrome_profile not found!")
        print("Please install the extension manually first:")
        print("  1. Run: start chrome --user-data-dir=chrome_profile --profile-directory=Default")
        print("  2. Install GoFullPage from Chrome Web Store")
        print("  3. Set keyboard shortcut to Ctrl+Shift+K")
        print("  4. Close Chrome and run this test again")
        sys.exit(1)
    
    print("\n[1/4] Starting Chrome with profile...")
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument(f'--user-data-dir={profile_dir}')
    chrome_options.add_argument('--profile-directory=Default')
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("   [OK] Chrome started")
    except Exception as e:
        print(f"   [ERROR] Failed to start Chrome: {str(e)}")
        sys.exit(1)
    
    # Navigate to a test page
    print("\n[2/4] Navigating to test page...")
    driver.get("https://www.example.com")
    time.sleep(3)
    print("   [OK] Page loaded")
    
    # Check extension is installed
    print("\n[3/4] Checking if extension is installed...")
    print("   Opening chrome://extensions/shortcuts in new tab...")
    driver.execute_script("window.open('chrome://extensions/shortcuts', '_blank');")
    time.sleep(2)
    
    # Switch to extensions tab
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    
    page_source = driver.page_source
    if "GoFullPage" in page_source:
        print("   [OK] GoFullPage extension found!")
        if "Ctrl+Shift+K" in page_source or "⌃⇧K" in page_source:
            print("   [OK] Keyboard shortcut Ctrl+Shift+K is configured!")
        else:
            print("   [WARNING] Keyboard shortcut might not be set to Ctrl+Shift+K")
            print("   Please go to chrome://extensions/shortcuts and set it manually")
    else:
        print("   [ERROR] GoFullPage extension NOT found!")
        print("   Please install it manually from Chrome Web Store")
        driver.quit()
        sys.exit(1)
    
    # Switch back to test page
    driver.switch_to.window(driver.window_handles[0])
    driver.close()  # Close extensions tab
    driver.switch_to.window(driver.window_handles[0])
    
    # Test keyboard shortcut
    print("\n[4/4] Testing keyboard shortcut Ctrl+Shift+K...")
    print("   Current tabs: ", len(driver.window_handles))
    
    # Trigger the shortcut
    keyboard = Controller()
    keyboard.press(Key.ctrl)
    time.sleep(0.05)
    keyboard.press(Key.shift)
    time.sleep(0.1)
    keyboard.press('k')
    time.sleep(0.05)
    keyboard.release('k')
    time.sleep(0.1)
    keyboard.release(Key.shift)
    time.sleep(0.05)
    keyboard.release(Key.ctrl)
    
    print("   [OK] Keyboard shortcut sent (Ctrl+Shift+K)")
    
    # Wait for extension to open new tab
    print("   Waiting 10 seconds for extension to respond...")
    time.sleep(10)
    
    # Check if new tab opened
    tabs_after = len(driver.window_handles)
    print(f"   Tabs after shortcut: {tabs_after}")
    
    if tabs_after > 1:
        print("\n" + "="*80)
        print("SUCCESS! Extension keyboard shortcut works!")
        print("="*80)
        print("The extension opened a new tab, which means the shortcut is working.")
        print("You should see the GoFullPage capture/download page in the new tab.")
        print("\nYour automation is ready to use!")
    else:
        print("\n" + "="*80)
        print("FAILED! Extension did not respond to keyboard shortcut")
        print("="*80)
        print("\nPossible issues:")
        print("1. Keyboard shortcut not set to Ctrl+Shift+K")
        print("   → Go to chrome://extensions/shortcuts")
        print("   → Find GoFullPage")
        print("   → Set to Ctrl+Shift+K")
        print("")
        print("2. Extension is disabled")
        print("   → Go to chrome://extensions/")
        print("   → Make sure GoFullPage is enabled")
        print("")
        print("3. Shortcut conflicts with another extension")
        print("   → Try a different shortcut like Alt+Shift+F")
        print("   → Update automation.py to match")
    
    print("\nBrowser will stay open for 5 seconds for inspection...")
    time.sleep(5)
    
    driver.quit()
    print("\n[COMPLETE] Test finished")

if __name__ == "__main__":
    test_extension_shortcut()

