"""
Quick script to run Excel processing test
"""
import subprocess
import sys

def main():
    print("="*60)
    print("EXCEL PROCESSING TEST RUNNER")
    print("="*60)
    print("This will test the Excel processing functionality:")
    print("1. Find downloaded Excel files")
    print("2. Add separator lines")
    print("3. Convert to PDF")
    print("="*60)
    
    try:
        # Run the Excel processing test
        result = subprocess.run([sys.executable, "test_excel_processing.py"], 
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ Excel processing test completed successfully!")
        else:
            print(f"\n❌ Excel processing test failed with return code: {result.returncode}")
            
    except Exception as e:
        print(f"\n❌ Error running test: {str(e)}")

if __name__ == "__main__":
    main()
