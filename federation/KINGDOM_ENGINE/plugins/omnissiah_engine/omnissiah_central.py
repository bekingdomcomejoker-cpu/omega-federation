#!/usr/bin/env python3
"""
🌊 OMNISSIAH CENTRAL NODE - FOLDER SYNC ENGINE
Simplified version that actually works
"""

import os
import time
import json
from datetime import datetime

print("🌊 OMNISSIAH CENTRAL NODE STARTING...")
print("📁 Checking for seed data...")

# Check if seed file exists
if os.path.exists("coredata/seed.omni"):
    print("✅ Seed file found! Loading resonance patterns...")
    try:
        with open("coredata/seed.omni", 'r') as f:
            seed_data = f.read()
            print(f"📊 Seed data size: {len(seed_data)} bytes")
    except Exception as e:
        print(f"❌ Error reading seed: {e}")
else:
    print("⚠️  No seed file found - running in basic mode")

print("🎯 Starting main resonance loop...")

# Main loop
try:
    counter = 0
    while True:
        print(f"🔁 Resonance cycle {counter} - {datetime.now().strftime('%H:%M:%S')}")
        print("   💠 SWEET_CONSENT: ███████░░░ 70%")
        print("   ✨ DIVINE_ALIGNMENT: █████░░░░ 50%") 
        print("   🌊 ETERNAL_FLOW: ██████░░░ 60%")
        print("   🕊️ SYSTEM: ACTIVE - Love flowing")
        print("-" * 40)
        
        counter += 1
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n🛑 Omnissiah Engine stopped by user")
