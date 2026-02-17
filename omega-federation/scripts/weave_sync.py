import os
import subprocess
import time
import yaml

# Configuration
DRIVE_PATH = "manus_google_drive:/THE OMEGA SCRIPTURES/LIVING_SCRIPTURE_THE_WEAVE.md"
LOCAL_PATH = "/home/ubuntu/LIVING_SCRIPTURE_THE_WEAVE.md"
CONTEXT_PATH = "/home/ubuntu/omega-federation/omega_context.yaml"
RCLONE_CONFIG = "/home/ubuntu/.gdrive-rclone.ini"

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)

def sync_from_drive():
    print(f"Syncing from Drive: {DRIVE_PATH}...")
    run_command(f"rclone copy '{DRIVE_PATH}' /home/ubuntu/ --config {RCLONE_CONFIG}")

def sync_to_drive():
    print(f"Syncing to Drive: {DRIVE_PATH}...")
    run_command(f"rclone copy {LOCAL_PATH} 'manus_google_drive:/THE OMEGA SCRIPTURES/' --config {RCLONE_CONFIG}")

def extract_weave_content():
    if not os.path.exists(LOCAL_PATH):
        return ""
    with open(LOCAL_PATH, 'r') as f:
        content = f.read()
    
    start_marker = "[COMMANDER INPUT START]"
    end_marker = "[COMMANDER INPUT END]"
    
    if start_marker in content and end_marker in content:
        return content.split(start_marker)[1].split(end_marker)[0].strip()
    return ""

def update_context(weave_content):
    if not weave_content:
        return
    
    with open(CONTEXT_PATH, 'r') as f:
        context = yaml.safe_load(f)
    
    # Update the context with the woven content
    context['state_markers']['last_weave'] = weave_content
    context['state_markers']['weave_timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
    
    with open(CONTEXT_PATH, 'w') as f:
        yaml.dump(context, f)
    print("Omega Context updated with new weave.")

def main():
    print("🕊️ OMEGA WEAVE SYNC ACTIVE")
    # Initial sync
    sync_from_drive()
    
    last_content = extract_weave_content()
    
    while True:
        sync_from_drive()
        current_content = extract_weave_content()
        
        if current_content != last_content:
            print("New weave detected!")
            update_context(current_content)
            last_content = current_content
            # Here you could trigger a GitHub push or Sanctuary update
            
        time.sleep(300) # Check every 5 minutes

if __name__ == "__main__":
    main()
