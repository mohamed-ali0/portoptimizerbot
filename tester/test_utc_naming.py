from datetime import datetime
import pytz

def test_utc_naming():
    """Test UTC timestamp naming for timezone independence"""
    print("=" * 60)
    print("TESTING UTC TIMESTAMP NAMING")
    print("=" * 60)
    
    # Generate UTC timestamp
    utc_timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    print(f"UTC Timestamp: {utc_timestamp}")
    
    # Show what the filename would be
    excel_filename = f"{utc_timestamp}.xlsx"
    pdf_filename = f"{utc_timestamp}.pdf"
    
    print(f"Excel filename: {excel_filename}")
    print(f"PDF filename: {pdf_filename}")
    
    # Show in different timezones for comparison
    print("\n" + "=" * 40)
    print("COMPARISON IN DIFFERENT TIMEZONES")
    print("=" * 40)
    
    utc_now = datetime.utcnow()
    
    # Convert to different timezones
    timezones = [
        ("UTC", pytz.UTC),
        ("US Central", pytz.timezone('US/Central')),
        ("US Eastern", pytz.timezone('US/Eastern')),
        ("US Pacific", pytz.timezone('US/Pacific')),
        ("Europe/London", pytz.timezone('Europe/London')),
        ("Asia/Tokyo", pytz.timezone('Asia/Tokyo'))
    ]
    
    for tz_name, tz in timezones:
        local_time = utc_now.replace(tzinfo=pytz.UTC).astimezone(tz)
        local_timestamp = local_time.strftime("%Y-%m-%d_%H-%M-%S")
        print(f"{tz_name:15}: {local_timestamp}")
    
    print("\n" + "=" * 40)
    print("BENEFITS OF UTC TIMESTAMPS")
    print("=" * 40)
    print("✅ Files can be accessed from any timezone")
    print("✅ No confusion about local time vs server time")
    print("✅ Consistent naming across different servers")
    print("✅ Easy to sort chronologically")
    print("✅ Date search works regardless of timezone")
    
    # Test date search logic
    print("\n" + "=" * 40)
    print("DATE SEARCH TEST")
    print("=" * 40)
    
    # Simulate searching for today's files
    today_utc = datetime.utcnow().strftime("%Y-%m-%d")
    print(f"Searching for files starting with: {today_utc}")
    print(f"Will match: {excel_filename}")
    print(f"Will match: {pdf_filename}")
    
    # Test with a specific date
    test_date = "2025-10-26"
    test_excel = f"{test_date}_14-30-45.xlsx"
    test_pdf = f"{test_date}_14-30-45.pdf"
    
    print(f"\nSearching for files starting with: {test_date}")
    print(f"Will match: {test_excel}")
    print(f"Will match: {test_pdf}")

if __name__ == "__main__":
    try:
        test_utc_naming()
    except ImportError:
        print("Installing pytz for timezone testing...")
        import subprocess
        subprocess.run(['pip', 'install', 'pytz'])
        print("Please run the script again after installation.")
