"""
Test script to verify win32gui keyboard shortcut works
This will send Ctrl+Shift+K to Chrome and wait 10 seconds
"""
import time
import win32gui
import win32con
from datetime import datetime

def test_win32gui_shortcut():
    """Test win32gui keyboard shortcut on Chrome"""
    print("="*80)
    print("WIN32GUI KEYBOARD SHORTCUT TEST")
    print("="*80)
    print("This will send Alt+M to Chrome window")
    print("Make sure Chrome is open and GoFullPage extension is installed")
    print("="*80)
    print()
    
    print("⏰ You have 10 seconds to:")
    print("   1. Open Chrome")
    print("   2. Make sure GoFullPage extension is installed")
    print("   3. Set GoFullPage shortcut to Alt+M")
    print("   4. Minimize RDP window (if using RDP)")
    print("   5. Click on Chrome to focus it")
    print()
    
    # Countdown
    for i in range(10, 0, -1):
        print(f"⏰ Starting in {i} seconds...", end='\r')
        time.sleep(1)
    
    print("\n🚀 Sending Alt+M to Chrome...")
    print("="*80)
    
    try:
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
            print(f"[{datetime.now()}] Found Chrome window, sending keyboard shortcut...")
            
            # Send Alt+M using win32gui
            # Hold Alt
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYDOWN, win32con.VK_MENU, 0)
            time.sleep(0.5)  # Hold Alt for 500ms
            
            # Press M
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYDOWN, ord('M'), 0)
            time.sleep(0.5)  # Hold M for 500ms
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYUP, ord('M'), 0)
            
            # Release Alt
            time.sleep(0.5)  # Wait 500ms before releasing Alt
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYUP, win32con.VK_MENU, 0)
            
            print(f"[{datetime.now()}] ✅ win32gui keyboard shortcut sent (Alt+M)")
            print(f"[{datetime.now()}] Check if GoFullPage extension triggered...")
            
            # Wait 10 seconds to see if extension works
            print(f"[{datetime.now()}] Waiting 10 seconds to see if extension responds...")
            for i in range(10, 0, -1):
                print(f"⏰ Waiting {i} seconds...", end='\r')
                time.sleep(1)
            
            print(f"\n[{datetime.now()}] Test complete!")
            print("Check if GoFullPage extension opened a new tab or captured screenshot")
            
        else:
            print(f"[{datetime.now()}] ❌ Chrome window not found")
            print("Make sure Chrome is open and visible")
            
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error: {str(e)}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    print("If GoFullPage extension triggered, you should see:")
    print("  - A new tab opened with screenshot result")
    print("  - Or a download started")
    print("  - Or extension popup appeared")
    print("="*80)
    
    # Wait for user to check results
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    test_win32gui_shortcut()
