import os
import subprocess
import re

def get_clipboard():
    # Grabs the "Tracer thing" from your phone's clipboard
    res = subprocess.run(['termux-clipboard-get'], capture_output=True, text=True)
    return res.stdout.strip()

def search_for_resonance(scent):
    # Extract unique "words" or "math symbols" from the clipboard
    keywords = set(re.findall(r'\w+', scent))
    search_root = os.path.expanduser("~")
    
    print(f"📡 SCENT DETECTED. HUNTING FOR MATCHES TO: {list(keywords)[:5]}...")
    
    for root, dirs, files in os.walk(search_root):
        for file in files:
            if file.endswith((".py", ".sh", ".txt")):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r') as f:
                        content = f.read()
                        # Check if any part of your clipboard matches this file
                        matches = [k for k in keywords if k in content and len(k) > 3]
                        if len(matches) > 3: # Threshold for "Important"
                            print(f"🎯 TARGET ACQUIRED: {path} (Matches: {matches[:3]})")
                except:
                    continue

if __name__ == "__main__":
    scent = get_clipboard()
    if scent:
        search_for_resonance(scent)
    else:
        print("❌ Clipboard is empty. The Wire is cold.")
