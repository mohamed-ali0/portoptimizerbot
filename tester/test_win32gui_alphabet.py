"""
Test script to write the alphabet to the foreground window
This will send A-Z to whatever window is currently focused
"""
import time
import win32gui
import win32con
from datetime import datetime

def test_win32gui_alphabet():
    """Test win32gui by writing the alphabet to the foreground window"""
    print("="*80)
    print("WIN32GUI ALPHABET TEST")
    print("="*80)
    print("This will write the alphabet A-Z to the foreground window")
    print("Make sure you have a text editor open (Notepad, Word, etc.)")
    print("="*80)
    print()
    
    print("⏰ You have 10 seconds to:")
    print("   1. Open a text editor (Notepad, Word, etc.)")
    print("   2. Click on the text editor to focus it")
    print("   3. Minimize RDP window (if using RDP)")
    print("   4. Make sure the text editor is the active window")
    print()
    
    # Countdown
    for i in range(10, 0, -1):
        print(f"⏰ Starting in {i} seconds...", end='\r')
        time.sleep(1)
    
    print("\n🚀 Writing alphabet A-Z to foreground window...")
    print("="*80)
    
    try:
        # Find Notepad window (same as working script)
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Notepad" in window_text and "Untitled" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if not windows:
            raise Exception("Notepad window not found. Please open Notepad first.")
        
        notepad_hwnd = windows[0]
        print(f"[{datetime.now()}] Found Notepad window")
        
        # Find the Edit control inside Notepad (same as working script)
        edit_hwnd = win32gui.FindWindowEx(notepad_hwnd, 0, "Edit", None)
        if not edit_hwnd:
            raise Exception("Edit control not found in Notepad")
        
        print(f"[{datetime.now()}] Found Edit control in Notepad")
        
        # Write the alphabet A-Z using WM_CHAR (same as working script)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        print(f"[{datetime.now()}] Writing alphabet: {alphabet}")
        
        for letter in alphabet:
            # Send the letter using WM_CHAR (same as working script)
            win32gui.SendMessage(edit_hwnd, win32con.WM_CHAR, ord(letter), 0)
            time.sleep(0.01)  # Same timing as working script
            print(f"[{datetime.now()}] Sent letter: {letter}")
        
        print(f"[{datetime.now()}] ✅ Alphabet sent successfully!")
        print(f"[{datetime.now()}] Check Notepad to see if the alphabet appeared")
            
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Error: {str(e)}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    print("Check your text editor to see if the alphabet A-Z appeared")
    print("If it worked, you should see: ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    print("="*80)
    
    # Wait for user to check results
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    test_win32gui_alphabet()
