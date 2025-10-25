from system_settings import SystemSettings

def test_settings():
    """Test if settings are actually read from JSON file"""
    print("=" * 50)
    print("TESTING SYSTEM SETTINGS")
    print("=" * 50)
    
    settings = SystemSettings()
    
    # Test reading from JSON file
    print(f"Frequency from JSON: {settings.get_frequency()} hours")
    print(f"Preferred hour from JSON: {settings.get_preferred_hour()}")
    print(f"Username from JSON: {settings.get_login_credentials()['username']}")
    print(f"Admin password valid: {settings.verify_admin_password('YB02Ss3JJdk')}")
    
    # Test updating and reading back
    print("\n" + "=" * 30)
    print("TESTING SETTINGS UPDATE")
    print("=" * 30)
    
    # Change preferred hour
    settings.set_preferred_hour(15)  # 3 PM
    print(f"Updated preferred hour to: {settings.get_preferred_hour()}")
    
    # Change frequency
    settings.set_frequency(12)  # 12 hours
    print(f"Updated frequency to: {settings.get_frequency()} hours")
    
    # Read all settings
    all_settings = settings.get_all_settings(include_passwords=False)
    print(f"All settings: {all_settings}")

if __name__ == "__main__":
    test_settings()
