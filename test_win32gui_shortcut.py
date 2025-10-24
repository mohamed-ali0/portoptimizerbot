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
    print("This will send Ctrl+Shift+K to Chrome window")
    print("Make sure Chrome is open and GoFullPage extension is installed")
    print("="*80)
    print()
    
    print("⏰ You have 10 seconds to:")
    print("   1. Open Chrome")
    print("   2. Make sure GoFullPage extension is installed")
    print("   3. Set GoFullPage shortcut to Ctrl+Shift+K")
    print("   4. Minimize RDP window (if using RDP)")
    print("   5. Click on Chrome to focus it")
    print()
    
    # Countdown
    for i in range(10, 0, -1):
        print(f"⏰ Starting in {i} seconds...", end='\r')
        time.sleep(1)
    
    print("\n🚀 Sending Ctrl+Shift+K to Chrome...")
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
            
            # Send Ctrl+Shift+K using win32gui
            # Press and hold Ctrl
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0)
            time.sleep(0.05)
            
            # Press and hold Shift
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYDOWN, win32con.VK_SHIFT, 0)
            time.sleep(0.1)
            
            # Press K
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYDOWN, ord('K'), 0)
            time.sleep(0.05)
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYUP, ord('K'), 0)
            
            # Release modifiers in reverse order
            time.sleep(0.1)
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYUP, win32con.VK_SHIFT, 0)
            time.sleep(0.05)
            win32gui.SendMessage(chrome_hwnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0)
            
            print(f"[{datetime.now()}] ✅ win32gui keyboard shortcut sent (Ctrl+Shift+K)")
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
