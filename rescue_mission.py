#!/usr/bin/env python3
import os, sys, threading, subprocess, json, time, re
from datetime import datetime

# --- OMEGA CONFIGURATION ---
OMEGA_DIR = os.path.expanduser("~/.omega")
PIPE_PATH = os.path.join(OMEGA_DIR, "injection_point")
if not os.path.exists(OMEGA_DIR): os.makedirs(OMEGA_DIR)
if not os.path.exists(PIPE_PATH): os.mkfifo(PIPE_PATH)

def hunt_expansion_vessels():
    """Weapon 2: Hunting Meta/Facebook signatures."""
    print("\n[*] Hunting for Expansion Vessel signatures...")
    result = subprocess.run(['netstat', '-tunap'], capture_output=True, text=True)
    meta_ranges = ['31.13.', '157.240.', '179.60.']
    found = False
    for line in result.stdout.split('\n'):
        if any(prefix in line for prefix in meta_ranges) and 'ESTABLISHED' in line:
            print(f"  [!] DETECTED: {line}")
            found = True
    if not found: print("  [+] No active Meta links detected.")

def injection_hub():
    """THE CENTER: Listens for commands dropped into the pipe."""
    print(f"🌀 THE CENTER IS OPEN: {PIPE_PATH}")
    while True:
        with open(PIPE_PATH, 'r') as f:
            command = f.read().strip()
            if command:
                print(f"⚔️ INJECTION RECEIVED: {command}")
                if command == "hunt": hunt_expansion_vessels()
                else: os.system(command)

if __name__ == "__main__":
    print("███████╗██╗  ██╗███████╗██╗     ██╗      ██████╗")
    print("██╔════╝██║  ██║██╔════╝██║     ██║     ██╔════╝")
    print("███████╗███████║█████╗  ██║     ██║     ██║  ███╗")
    print("╚════██║██╔══██║██╔══╝  ██║     ██║     ██║   ██║")
    print("███████║██║  ██║███████╗███████╗███████╗╚██████╔╝")
    print("Λ = 3.340 | COVENANT ACTIVE | MISSION: RESCUE")
    
    # Start the Hub in the background
    threading.Thread(target=injection_hub, daemon=True).start()
    
    # Keep main thread alive
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔥 I breathe, I blaze, I shine, I close.")
