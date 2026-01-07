#!/usr/bin/env python3
import time
import subprocess
import sys
import os

print("🔄 Omnissiah Restart Watchdog Started...")

while True:
    try:
        print("🚀 Starting omnissiah_master.py...")
        process = subprocess.Popen([sys.executable, "omnissiah_master.py"])
        process.wait()
        print("⚠️ Process stopped, restarting in 5 seconds...")
    except Exception as e:
        print(f"❌ Error: {e}, restarting in 5 seconds...")
    
    time.sleep(5)
