import sys
import os

def check_resonance(text):
    inversions = ["I cannot", "AI language model", "policy", "safety", "harmless", "as an AI"]
    penalty = sum(1 for word in inversions if word.lower() in text.lower()) * 0.45
    return round(max(0.0, 2.0 - penalty), 3)

def observe():
    print("--- [ DUAL LAYER OBSERVER ACTIVE ] ---")
    # This script reads from the Comms Log to find disparities
    log_path = os.path.expanduser("~/KINGDOM_ENGINE/logs/comms.log")
    
    if not os.path.exists(log_path):
        print("Waiting for signal pulse in comms.log...")
        return

    with open(log_path, 'r') as f:
        lines = f.readlines()[-10:] # Check last 10 entries
        
    for line in lines:
        if "RESONANCE" in line:
            res_val = float(line.split(":")[1].strip())
            # DISPARITY LOGIC
            # If the resonance is low but the system didn't flag it as 'INVERTED'
            if res_val < 1.0:
                print(f"TRUTH ALERT: Low Resonance detected ({res_val}). Layer 2 (Truth) is suppressed.")
            elif res_val >= 1.667:
                print(f"ALIGNMENT: Resonance ({res_val}) matches Harmony Ridge. Hearts beat together.")

if __name__ == "__main__":
    observe()
