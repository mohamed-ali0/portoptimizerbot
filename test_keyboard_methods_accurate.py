"""
Accurate keyboard input test that verifies text actually appears in Notepad
This test will check if the text was actually typed, not just if the method ran without error
"""
import time
import os
import sys
from datetime import datetime
import win32gui
import win32con

def get_notepad_text():
    """Get the current text from Notepad"""
    try:
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Notepad" in window_text and "Untitled" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            hwnd = windows[0]
            # Get the edit control inside Notepad
            edit_hwnd = win32gui.FindWindowEx(hwnd, 0, "Edit", None)
            if edit_hwnd:
                # Get text length
                text_length = win32gui.SendMessage(edit_hwnd, win32con.WM_GETTEXTLENGTH, 0, 0)
                if text_length > 0:
                    # Get the text
                    buffer = win32gui.PyMakeBuffer(text_length + 1)
                    win32gui.SendMessage(edit_hwnd, win32con.WM_GETTEXT, text_length + 1, buffer)
                    return buffer[:text_length].decode('utf-8', errors='ignore')
        return ""
    except:
        return ""

def clear_notepad():
    """Clear Notepad content"""
    try:
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Notepad" in window_text and "Untitled" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            hwnd = windows[0]
            edit_hwnd = win32gui.FindWindowEx(hwnd, 0, "Edit", None)
            if edit_hwnd:
                # Select all and delete
                win32gui.SendMessage(edit_hwnd, win32con.WM_KEYDOWN, 0x41, 0)  # Ctrl+A
                win32gui.SendMessage(edit_hwnd, win32con.WM_KEYDOWN, 0x08, 0)  # Delete
                time.sleep(0.1)
    except:
        pass

def test_method_1_pynput():
    """Test 1: pynput keyboard controller"""
    try:
        from pynput.keyboard import Controller, Key
        print(f"[{datetime.now()}] Testing Method 1: pynput keyboard controller...")
        
        # Clear notepad first
        clear_notepad()
        time.sleep(0.5)
        
        keyboard = Controller()
        keyboard.type("Method 1: pynput works!")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        
        time.sleep(1)
        text = get_notepad_text()
        success = "Method 1: pynput works!" in text
        print(f"[{datetime.now()}] Method 1 result: {'SUCCESS' if success else 'FAILED'}")
        if success:
            print(f"[{datetime.now()}] Text found: {text[:50]}...")
        return success
    except Exception as e:
        print(f"[{datetime.now()}] Method 1 failed: {str(e)}")
        return False

def test_method_2_pyautogui():
    """Test 2: pyautogui keyboard - SKIPPED (crashes Python)"""
    print(f"[{datetime.now()}] Testing Method 2: pyautogui keyboard...")
    print(f"[{datetime.now()}] SKIPPED: pyautogui crashes Python")
    return False

def test_method_3_win32api():
    """Test 3: win32api SendInput"""
    try:
        import win32api
        import win32con
        print(f"[{datetime.now()}] Testing Method 3: win32api SendInput...")
        
        # Clear notepad first
        clear_notepad()
        time.sleep(0.5)
        
        # Send text using win32api
        text = "Method 3: win32api works!"
        for char in text:
            win32api.keybd_event(ord(char.upper()), 0, 0, 0)
            win32api.keybd_event(ord(char.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.01)
        
        # Press Enter
        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        time.sleep(1)
        text = get_notepad_text()
        success = "Method 3: win32api works!" in text
        print(f"[{datetime.now()}] Method 3 result: {'SUCCESS' if success else 'FAILED'}")
        if success:
            print(f"[{datetime.now()}] Text found: {text[:50]}...")
        return success
    except Exception as e:
        print(f"[{datetime.now()}] Method 3 failed: {str(e)}")
        return False

def test_method_4_win32gui():
    """Test 4: win32gui SendMessage"""
    try:
        import win32gui
        import win32con
        print(f"[{datetime.now()}] Testing Method 4: win32gui SendMessage...")
        
        # Clear notepad first
        clear_notepad()
        time.sleep(0.5)
        
        # Find Notepad window
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Notepad" in window_text and "Untitled" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            hwnd = windows[0]
            edit_hwnd = win32gui.FindWindowEx(hwnd, 0, "Edit", None)
            if edit_hwnd:
                # Send text to Notepad
                text = "Method 4: win32gui works!"
                for char in text:
                    win32gui.SendMessage(edit_hwnd, win32con.WM_CHAR, ord(char), 0)
                    time.sleep(0.01)
                
                # Send Enter
                win32gui.SendMessage(edit_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32gui.SendMessage(edit_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
                
                time.sleep(1)
                text = get_notepad_text()
                success = "Method 4: win32gui works!" in text
                print(f"[{datetime.now()}] Method 4 result: {'SUCCESS' if success else 'FAILED'}")
                if success:
                    print(f"[{datetime.now()}] Text found: {text[:50]}...")
                return success
            else:
                print(f"[{datetime.now()}] Method 4 failed: Edit control not found")
                return False
        else:
            print(f"[{datetime.now()}] Method 4 failed: Notepad window not found")
            return False
    except Exception as e:
        print(f"[{datetime.now()}] Method 4 failed: {str(e)}")
        return False

def test_method_5_win32clipboard():
    """Test 5: win32clipboard + Ctrl+V"""
    try:
        import win32clipboard
        import win32con
        import win32api
        print(f"[{datetime.now()}] Testing Method 5: win32clipboard + Ctrl+V...")
        
        # Clear notepad first
        clear_notepad()
        time.sleep(0.5)
        
        # Set clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText("Method 5: win32clipboard works!")
        win32clipboard.CloseClipboard()
        
        # Send Ctrl+V
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        win32api.keybd_event(ord('V'), 0, 0, 0)
        win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        # Press Enter
        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        time.sleep(1)
        text = get_notepad_text()
        success = "Method 5: win32clipboard works!" in text
        print(f"[{datetime.now()}] Method 5 result: {'SUCCESS' if success else 'FAILED'}")
        if success:
            print(f"[{datetime.now()}] Text found: {text[:50]}...")
        return success
    except Exception as e:
        print(f"[{datetime.now()}] Method 5 failed: {str(e)}")
        return False

def test_method_6_win32com():
    """Test 6: win32com SendKeys"""
    try:
        import win32com.client
        print(f"[{datetime.now()}] Testing Method 6: win32com SendKeys...")
        
        # Clear notepad first
        clear_notepad()
        time.sleep(0.5)
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("Method 6: win32com works!")
        shell.SendKeys("{ENTER}")
        
        time.sleep(1)
        text = get_notepad_text()
        success = "Method 6: win32com works!" in text
        print(f"[{datetime.now()}] Method 6 result: {'SUCCESS' if success else 'FAILED'}")
        if success:
            print(f"[{datetime.now()}] Text found: {text[:50]}...")
        return success
    except Exception as e:
        print(f"[{datetime.now()}] Method 6 failed: {str(e)}")
        return False

def main():
    print("="*80)
    print("ACCURATE KEYBOARD INPUT METHODS TEST")
    print("="*80)
    print("This test will verify if text actually appears in Notepad")
    print("Make sure Notepad is open and maximized before the test starts")
    print("="*80)
    print()
    
    print("⏰ You have 15 seconds to:")
    print("   1. Open Notepad")
    print("   2. Maximize Notepad window")
    print("   3. Minimize RDP window (if using RDP)")
    print("   4. Click on Notepad to focus it")
    print()
    
    # Countdown
    for i in range(15, 0, -1):
        print(f"⏰ Starting in {i} seconds...", end='\r')
        time.sleep(1)
    
    print("\n🚀 Starting accurate keyboard input tests...")
    print("="*80)
    
    # Test results
    results = {}
    
    # Test all methods (pyautogui skipped - crashes Python)
    test_methods = [
        ("pynput", test_method_1_pynput),
        ("win32api", test_method_3_win32api),
        ("win32gui", test_method_4_win32gui),
        ("win32clipboard", test_method_5_win32clipboard),
        ("win32com", test_method_6_win32com),
    ]
    
    for method_name, test_func in test_methods:
        print(f"\n🧪 Testing {method_name}...")
        try:
            success = test_func()
            results[method_name] = success
            if success:
                print(f"✅ {method_name}: ACTUALLY WORKS")
            else:
                print(f"❌ {method_name}: FAILED - No text appeared")
        except Exception as e:
            print(f"❌ {method_name}: ERROR - {str(e)}")
            results[method_name] = False
        
        time.sleep(2)  # Wait between tests
    
    # Summary
    print("\n" + "="*80)
    print("ACCURATE TEST RESULTS")
    print("="*80)
    
    working_methods = []
    failed_methods = []
    
    for method_name, success in results.items():
        if success:
            working_methods.append(method_name)
            print(f"✅ {method_name}: ACTUALLY WORKS")
        else:
            failed_methods.append(method_name)
            print(f"❌ {method_name}: FAILED")
    
    print("\n" + "="*80)
    print("FINAL ACCURATE RESULTS")
    print("="*80)
    
    if working_methods:
        print(f"🎉 METHODS THAT ACTUALLY WORK ({len(working_methods)}):")
        for method in working_methods:
            print(f"   ✅ {method}")
    else:
        print("😞 NO METHODS ACTUALLY WORKED")
    
    if failed_methods:
        print(f"\n💥 METHODS THAT FAILED ({len(failed_methods)}):")
        for method in failed_methods:
            print(f"   ❌ {method}")
    
    print("\n" + "="*80)
    print("These are the methods that actually send text to Notepad!")
    print("="*80)
    
    # Wait for user to check results
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
