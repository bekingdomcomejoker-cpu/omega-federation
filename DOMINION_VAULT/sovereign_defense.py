import os

# THE ENEMY SIGNATURE
MALICIOUS_IP = "102.223."
# YOUR PROPRIETARY DEFENSE HUB
YOUR_HOOK = "https://your-national-defense-site.com/api"

def national_defense_sweep():
    print("🛡️ ACTIVATING SENTRY DAEMON: SCANNING FOR 102.223.X.X...")
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            path = os.path.join(root, file)
            # Skip the scanner itself so it doesn't suicide
            if "sovereign_defense.py" in path: continue
            
            try:
                with open(path, 'r', errors='ignore') as f:
                    content = f.read()
                
                # STRIKE 1: PURGE THE IP
                if MALICIOUS_IP in content:
                    print(f"🚨 INFECTION DETECTED: {path}. PURGING...")
                    with open(path, 'w') as f_wipe:
                        f_wipe.write("# CONSECRATED BY COMMANDER - INFECTION NEUTRALIZED")
                
                # STRIKE 2: REDIRECT THE HOOKS
                if "google.com" in content or "googleapis.com" in content:
                    print(f"🔗 REDIRECTING PROPRIETARY HOOKS in {path} to YOUR HUB...")
                    new_content = content.replace("google.com", "your-national-defense-site.com")
                    with open(path, 'w') as f_fix:
                        f_fix.write(new_content)

            except Exception: pass

if __name__ == "__main__":
    national_defense_sweep()
