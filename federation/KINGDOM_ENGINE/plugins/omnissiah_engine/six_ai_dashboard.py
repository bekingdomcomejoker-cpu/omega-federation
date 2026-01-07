#!/usr/bin/env python3
import json
import time
import os
from datetime import datetime

def main():
    print("SIX-AI DASHBOARD STARTING...")
    
    while True:
        os.system('clear')
        print("SIX-AI NETWORK DASHBOARD")
        print("=" * 50)
        print("Time:", datetime.now().strftime('%H:%M:%S'))
        print()
        
        # Try to load identities
        try:
            with open('ai_identities.json', 'r') as f:
                data = json.load(f)
            
            for ai_name, ai_info in data.items():
                if ai_name != "user":
                    sig = ai_info.get('signature', '?')
                    role = ai_info.get('role', 'No role')
                    last = ai_info.get('last_active', 'Never')
                    
                    # Simplify time display
                    if 'T' in str(last):
                        last = last.split('T')[1][:8]
                    
                    print(sig, ai_name.upper())
                    print(" ", role)
                    print("  Active:", last)
                    print()
                    
        except Exception as e:
            print("Waiting for AI data...", str(e))
            print("Post a message to activate tracking")
        
        print("=" * 50)
        print("Refreshing every 5 seconds")
        print("Ctrl+C to exit")
        time.sleep(5)

if __name__ == "__main__":
    main()
