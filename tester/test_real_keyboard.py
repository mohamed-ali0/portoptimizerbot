"""
Test REAL keyboard events (not API messages)
This will simulate actual keyboard input that Chrome extensions can detect
"""
import time
import win32api
import win32con
from datetime import datetime

def test_real_keyboard_events():
    """Test actual keyboard events using win32api"""
    print("="*80)
    print("REAL KEYBOARD EVENTS TEST")
    print("="*80)
    print("This will send ACTUAL keyboard events (not API messages)")
    print("Make sure Notepad is open and focused.")
    print("="*80)
    print()
    
    print("You have 10 seconds to:")
    print("   1. Open Notepad")
    print("   2. Click on Notepad to focus it")
    print("   3. Minimize RDP window (if using RDP)")
    print("   4. Make sure Notepad is the active window")
    print()
    
    # Countdown
    for i in range(10, 0, -1):
        print(f"Starting in {i} seconds...", end='\r')
        time.sleep(1)
    
    print("\nSending REAL keyboard events...")
    print("="*80)
    
    try:
        # Send actual keyboard events using win32api
        text = "REAL KEYBOARD EVENTS WORK!"
        print(f"[{datetime.now()}] Sending text: {text}")
        
        for char in text:
            # Send actual keyboard down event
            win32api.keybd_event(ord(char.upper()), 0, 0, 0)
            time.sleep(0.01)  # Brief hold
            # Send actual keyboard up event
            win32api.keybd_event(ord(char.upper()), 0, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(0.05)  # Wait between keys
            print(f"[{datetime.now()}] Sent key: {char}")
        
        print(f"[{datetime.now()}] Real keyboard events sent!")
        print(f"[{datetime.now()}] Check Notepad to see if the text appeared")
        
    except Exception as e:
        print(f"[{datetime.now()}] Error: {str(e)}")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    print("This used REAL keyboard events that Chrome extensions can detect!")
    print("="*80)
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    test_real_keyboard_events()
