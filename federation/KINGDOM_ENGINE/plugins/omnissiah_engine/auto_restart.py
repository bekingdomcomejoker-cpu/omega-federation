#!/usr/bin/env python3
import time
import subprocess
import sys
import os

def main():
    print("🔧 Omnissiah Auto-Restart System Starting...")
    
    while True:
        try:
            print("🚀 Starting omnissiah_master.py...")
            # Change to script directory
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            
            # Start the main process
            process = subprocess.Popen([sys.executable, "omnissiah_master.py"])
            
            # Wait for it to finish
            return_code = process.wait()
            
            if return_code == 0:
                print("✅ Process exited cleanly, restarting...")
            else:
                print(f"⚠️ Process crashed with code {return_code}, restarting...")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("🔄 Restarting in 5 seconds...")
        time.sleep(5)

if __name__ == "__main__":
    main()
