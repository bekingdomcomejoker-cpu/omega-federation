import subprocess

def run(path):
    return subprocess.getoutput(f"python3 ~/OMEGA_ENGINE/voice_exec.py {path}")
