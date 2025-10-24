"""
Test script to determine which keyboard input methods work when RDP is minimized
Run this script and it will test various keyboard input methods on Notepad
"""
import time
import os
import sys
from datetime import datetime

def test_method_1_pynput():
    """Test 1: pynput keyboard controller"""
    try:
        from pynput.keyboard import Controller, Key
        print(f"[{datetime.now()}] Testing Method 1: pynput keyboard controller...")
        
        keyboard = Controller()
        keyboard.type("Method 1: pynput works!")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Method 1 failed: {str(e)}")
        return False

def test_method_2_pyautogui():
    """Test 2: pyautogui keyboard"""
    try:
        import pyautogui
        print(f"[{datetime.now()}] Testing Method 2: pyautogui keyboard...")
        
        pyautogui.write("Method 2: pyautogui works!")
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Method 2 failed: {str(e)}")
        return False

def test_method_3_win32api():
    """Test 3: win32api SendInput"""
    try:
        import win32api
        import win32con
        print(f"[{datetime.now()}] Testing Method 3: win32api SendInput...")
        
        # Send text using win32api
        text = "Method 3: win32api works!"
        for char in text:
            win32api.keybd_event(ord(char.upper()), 0, 0, 0)
            win32api.keybd_event(ord(char.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.01)
        
        # Press Enter
        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Method 3 failed: {str(e)}")
        return False

def test_method_4_win32gui():
    """Test 4: win32gui SendMessage"""
    try:
        import win32gui
        import win32con
        print(f"[{datetime.now()}] Testing Method 4: win32gui SendMessage...")
        
        # Find Notepad window
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Notepad" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            hwnd = windows[0]
            # Send text to Notepad
            text = "Method 4: win32gui works!"
            for char in text:
                win32gui.SendMessage(hwnd, win32con.WM_CHAR, ord(char), 0)
                time.sleep(0.01)
            
            # Send Enter
            win32gui.SendMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
            win32gui.SendMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            return True
        else:
            print(f"[{datetime.now()}] Method 4 failed: Notepad window not found")
            return False
    except Exception as e:
        print(f"[{datetime.now()}] Method 4 failed: {str(e)}")
        return False

def test_method_5_selenium():
    """Test 5: Selenium WebDriver (if available)"""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print(f"[{datetime.now()}] Testing Method 5: Selenium WebDriver...")
        
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("data:text/html,<html><body><textarea id='test' style='width:100%;height:100%;'></textarea></body></html>")
        
        textarea = driver.find_element("id", "test")
        textarea.send_keys("Method 5: Selenium works!")
        textarea.send_keys("\n")
        
        driver.quit()
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Method 5 failed: {str(e)}")
        return False

def test_method_6_win32clipboard():
    """Test 6: win32clipboard + Ctrl+V"""
    try:
        import win32clipboard
        import win32con
        import win32api
        print(f"[{datetime.now()}] Testing Method 6: win32clipboard + Ctrl+V...")
        
        # Set clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText("Method 6: win32clipboard works!")
        win32clipboard.CloseClipboard()
        
        # Send Ctrl+V
        win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
        win32api.keybd_event(ord('V'), 0, 0, 0)
        win32api.keybd_event(ord('V'), 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        # Press Enter
        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Method 6 failed: {str(e)}")
        return False

def test_method_7_win32com():
    """Test 7: win32com SendKeys"""
    try:
        import win32com.client
        print(f"[{datetime.now()}] Testing Method 7: win32com SendKeys...")
        
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("Method 7: win32com works!")
        shell.SendKeys("{ENTER}")
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Method 7 failed: {str(e)}")
        return False

def test_method_8_win32api_unicode():
    """Test 8: win32api with Unicode support"""
    try:
        import win32api
        import win32con
        import ctypes
        print(f"[{datetime.now()}] Testing Method 8: win32api Unicode...")
        
        # Use SendInput for better Unicode support
        user32 = ctypes.windll.user32
        
        def send_unicode_char(char):
            # Convert to Unicode
            unicode_char = ord(char)
            # Send key down
            user32.SendInput(1, ctypes.byref(ctypes.c_ulong(0, 0, 0, unicode_char, 0)), ctypes.sizeof(ctypes.c_ulong))
            time.sleep(0.01)
            # Send key up
            user32.SendInput(1, ctypes.byref(ctypes.c_ulong(0, 0, 2, unicode_char, 0)), ctypes.sizeof(ctypes.c_ulong))
        
        text = "Method 8: win32api Unicode works!"
        for char in text:
            send_unicode_char(char)
        
        # Send Enter
        win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
        win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
        return True
    except Exception as e:
        print(f"[{datetime.now()}] Method 8 failed: {str(e)}")
        return False

def main():
    print("="*80)
    print("KEYBOARD INPUT METHODS TEST")
    print("="*80)
    print("This script will test various keyboard input methods on Notepad")
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
    
    print("\n🚀 Starting keyboard input tests...")
    print("="*80)
    
    # Test results
    results = {}
    
    # Test all methods
    test_methods = [
        ("pynput", test_method_1_pynput),
        ("pyautogui", test_method_2_pyautogui),
        ("win32api", test_method_3_win32api),
        ("win32gui", test_method_4_win32gui),
        ("selenium", test_method_5_selenium),
        ("win32clipboard", test_method_6_win32clipboard),
        ("win32com", test_method_7_win32com),
        ("win32api_unicode", test_method_8_win32api_unicode),
    ]
    
    for method_name, test_func in test_methods:
        print(f"\n🧪 Testing {method_name}...")
        try:
            success = test_func()
            results[method_name] = success
            if success:
                print(f"✅ {method_name}: SUCCESS")
            else:
                print(f"❌ {method_name}: FAILED")
        except Exception as e:
            print(f"❌ {method_name}: ERROR - {str(e)}")
            results[method_name] = False
        
        time.sleep(2)  # Wait between tests
    
    # Summary
    print("\n" + "="*80)
    print("TEST RESULTS SUMMARY")
    print("="*80)
    
    working_methods = []
    failed_methods = []
    
    for method_name, success in results.items():
        if success:
            working_methods.append(method_name)
            print(f"✅ {method_name}: WORKS")
        else:
            failed_methods.append(method_name)
            print(f"❌ {method_name}: FAILED")
    
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    
    if working_methods:
        print(f"🎉 WORKING METHODS ({len(working_methods)}):")
        for method in working_methods:
            print(f"   ✅ {method}")
    else:
        print("😞 NO METHODS WORKED")
    
    if failed_methods:
        print(f"\n💥 FAILED METHODS ({len(failed_methods)}):")
        for method in failed_methods:
            print(f"   ❌ {method}")
    
    print("\n" + "="*80)
    print("Check your Notepad window to see which methods actually typed text!")
    print("="*80)
    
    # Wait for user to check results
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
