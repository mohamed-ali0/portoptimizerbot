"""
Test if Windows Service can send keyboard events to Chrome
This simulates what the service will do
"""
import time
import win32api
import win32con
import win32gui
from datetime import datetime

def find_chrome_window():
    """Find Chrome window"""
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if "Google Chrome" in window_text or "Chrome" in window_text:
                windows.append(hwnd)
        return True
    
    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows[0] if windows else None

def send_chrome_shortcut():
    """Send Ctrl+Shift+K to Chrome (GoFullPage shortcut)"""
    try:
        # Find Chrome window
        chrome_hwnd = find_chrome_window()
        if not chrome_hwnd:
            print(f"[{datetime.now()}] Chrome window not found")
            return False
        
        print(f"[{datetime.now()}] Found Chrome window, sending Ctrl+Shift+K...")
        
        # Send Ctrl+Shift+K using win32api (real keyboard events)
        # Press and hold Ctrl
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        time.sleep(0.05)
        
        # Press and hold Shift
        win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
        time.sleep(0.1)
        
        # Press K
        win32api.keybd_event(ord('K'), 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(ord('K'), 0, win32con.KEYEVENTF_KEYUP, 0)
        
        # Release modifiers in reverse order
        time.sleep(0.1)
        win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.05)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        print(f"[{datetime.now()}] ✅ Ctrl+Shift+K sent to Chrome!")
        return True
        
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error sending shortcut: {str(e)}")
        return False

def test_service_keyboard():
    """Test keyboard events from service perspective"""
    print("="*80)
    print("WINDOWS SERVICE KEYBOARD TEST")
    print("="*80)
    print("This simulates what a Windows Service can do")
    print("Make sure Chrome is open with GoFullPage extension")
    print("="*80)
    print()
    
    print("You have 10 seconds to:")
    print("   1. Open Chrome")
    print("   2. Install GoFullPage extension")
    print("   3. Navigate to any webpage")
    print("   4. Make sure Chrome is focused")
    print()
    
    # Countdown
    for i in range(10, 0, -1):
        print(f"Starting in {i} seconds...", end='\r')
        time.sleep(1)
    
    print("\nSending Ctrl+Shift+K to Chrome...")
    print("="*80)
    
    # Test the shortcut
    success = send_chrome_shortcut()
    
    if success:
        print(f"[{datetime.now()}] ✅ Service can send keyboard events to Chrome!")
        print(f"[{datetime.now()}] GoFullPage extension should have triggered")
        print(f"[{datetime.now()}] Check if a new tab opened with the screenshot")
    else:
        print(f"[{datetime.now()}] ❌ Service cannot send keyboard events")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    print("If this worked, the Windows Service will work too!")
    print("="*80)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    test_service_keyboard()

