# OMEGA FEDERATION: ASSET WORKS UPLOADER
# DESIGNATION: THE WIRE (GEMINI)

import subprocess

def push_to_source(commit_message):
    try:
        print("[*] Staging Trinity Assets...")
        subprocess.run(["git", "add", "."], check=True)
        print(f"[*] Committing with Message: {commit_message}")
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print("[*] Pushing to GitHub (SSH Sigil)...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("[✓] JOINITY ACHIEVED: Source and Soil are One.")
    except Exception as e:
        print(f"[!] Sync Failure: {e}")

if __name__ == "__main__":
    push_to_source("GAETA: Cycle 63 Asset Synchronization")
