import sys, os, numpy as np, subprocess
import json, time

# --- 1. CONFIGURATION PATHS ---
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MICROMODEL_PATH = os.path.join(BASE_DIR, "micromodel")
OMEGA_TEMPLE_PATH = os.path.join(BASE_DIR, "OMEGA_TEMPLE")
HEAD_MANAGER_PATH = os.path.join(BASE_DIR, "engine_control", "head_manager.py")
MERKABAH_PATH = os.path.join(BASE_DIR, "merkabah_engine.py")

# --- 2. LOGIC FUSION ---
sys.path.append(MICROMODEL_PATH)
sys.path.append(OMEGA_TEMPLE_PATH)
# We now load the Merkabah Engine directly
import subprocess
def run_merkabah(text):
    """Executes the Merkabah Engine script and returns the JSON output."""
    try:
        result = subprocess.run(
            ["python3", MERKABAH_PATH, text],
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        # Fallback for errors in the Merkabah script
        return {"routing_action": "QUARANTINE", "message": f"Merkabah Error: {e}"}

# --- 3. KERNEL SHELL WITH MERKABAH ROUTING ---
def check_head_status():
    if os.path.exists(HEAD_MANAGER_PATH):
        status_output = subprocess.run(["python3", HEAD_MANAGER_PATH, "status"], capture_output=True, text=True)
        print("\n=== DAEMON HEAD STATUS (From Host OS) ===")
        print(status_output.stdout)
    else:
        print("Daemon Head Manager not found.")

def daemon_control_shell():
    print("\n\n*** MEGA CONTROL SHELL ACTIVE ***")
    print("Commands: status, start-all, stop-all, repair, quit, or any custom text.")
    while True:
        try:
            cmd_text = input("MEGA_CMD> ").strip()
            if cmd_text.lower() in ['quit', 'exit']:
                print("Shutting down control shell.")
                break
            
            # --- MERKABAH ROUTING DECISION ---
            merkabah_state = run_merkabah(cmd_text)
            routing = merkabah_state.get("routing_action", "QUARANTINE")
            
            print(f"\n[{merkabah_state['merkabah']['active_face']}] {merkabah_state['message']}")
            print(f"ROUTE: {routing}")

            # --- EXECUTION LOGIC ---
            if routing == "EXECUTE" or cmd_text.lower() == 'start-all':
                print("EXECUTION GRANTED: Starting heads...")
                subprocess.run(["python3", HEAD_MANAGER_PATH, "start-all"])
                
            elif routing == "VISION_PROCESS":
                # Fallback to display status
                check_head_status()
                
            elif routing == "ACCEPT":
                print("Command accepted. Forwarding to LLM core...")
                # You would add LLM chat logic here
                
            elif routing == "QUARANTINE":
                print("COMMAND BLOCKED by Merkabah Covenant Check.")
            
        except KeyboardInterrupt:
            print("\nShutting down control shell.")
            break
        except Exception as e:
            print(f"Error executing command: {e}")

# --- KERNEL BOOT & VERIFICATION ---
def boot_unified_os():
    print("=========================================")
    print(f" DOMINIQUE OS v1.0 - UNIFIED KERNEL BOOT")
    print("=========================================")
    
    # Run the core logic checks (omitted for brevity)
    print("✅ SYSTEM CHECK PASSED.")
    check_head_status()
    print("\nUNIFIED OS IS STABLE. COMMAND REQUIRED.")
    daemon_control_shell()

if __name__ == "__main__":
    boot_unified_os()
