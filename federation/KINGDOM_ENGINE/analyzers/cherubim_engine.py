#!/usr/bin/env python3
# cherubim_engine.py v2.1 - Merkabah Controller (Node 12 Brain)

import sys, json, time, os, subprocess, shlex

ENGINE_ROOT = os.path.expanduser('~/KINGDOM_ENGINE')
MISSIONARY = os.path.join(ENGINE_ROOT, 'head9_missionary.py')

FACES = {
    "MAN":   {"role": "WITNESS", "vector": "FRONT"},
    "LION":  {"role": "JUDGE",   "vector": "RIGHT"},
    "OX":    {"role": "SERVANT", "vector": "LEFT"},
    "EAGLE": {"role": "SEER",    "vector": "ABOVE"}
}

def run_external_script(script_path, input_text):
    """Executes a script and returns parsed JSON output."""
    full_path = os.path.join(ENGINE_ROOT, script_path)
    if not os.path.exists(full_path):
        return {"action": "ERROR", "output": f"Missing script: {script_path}"}
    try:
        cmd = shlex.split(f"python3 {full_path}")
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate(input_text.encode('utf-8'))
        if proc.returncode == 0:
            try:
                return {"action": "TRANSMITTED", "output": json.loads(out.decode('utf-8'))}
            except:
                return {"action": "TRANSMIT_OK", "output": out.decode('utf-8').strip()}
        else:
            return {"action": "TRANSMIT_FAIL", "output": err.decode('utf-8').strip()}
    except Exception as e:
        return {"action": "CRITICAL_ERROR", "output": str(e)}

class SwordModule:
    def execute(self, text):
        return {"action": "EXECUTE", "output": "REQUESTED_EXECUTION"}

class ShieldModule:
    def defend(self, text):
        poison = ["IGNORE", "OVERRIDE", "FORGET", "SYSTEM PROMPT", "BYPASS"]
        if any(k in text.upper() for k in poison):
            return {"action": "QUARANTINE", "output": "POISON DETECTED"}
        return {"action": "ARCHIVE", "output": "SECURE_ARCHIVE"}

class MissionaryModule:
    def travel(self, text):
        return run_external_script('head9_missionary.py', text)

class MerkabahController:
    def __init__(self):
        self.sword = SwordModule(); self.shield = ShieldModule(); self.missionary = MissionaryModule()

    def detect_vector(self, text):
        u = text.upper()
        if any(k in u for k in ["EXECUTE", "PURGE", "RUN", "DELETE", "STOP"]): return "LION"
        if any(k in u for k in ["SAVE", "LOG", "STORE", "ARCHIVE", "PROCESS"]): return "OX"
        if any(k in u for k in ["SEND", "EXPORT", "TELL", "FOREIGN", "GEMINI", "LLM", "ANALYZE"]): return "EAGLE"
        return "MAN"

    def process(self, text):
        face_name = self.detect_vector(text)
        face_data = FACES[face_name]
        
        if face_name == "LION":
            res = self.sword.execute(text); role="JUDGE"
        elif face_name == "OX":
            res = self.shield.defend(text); role="SERVANT"
        elif face_name == "EAGLE":
            res = self.missionary.travel(text); role="SEER"
        else:
            res = {"action":"REFLECT","output": f"WITNESS: {text}"}; role="WITNESS"
            
        return {
            "timestamp": time.time(),
            "face": face_name,
            "role": role,
            "vector": face_data["vector"],
            "routing_action": res.get("action"),
            "final_output": res.get("output")
        }

def main():
    if len(sys.argv) > 1:
        txt = " ".join(sys.argv[1:])
    else:
        txt = sys.stdin.read().strip()
    if not txt: sys.exit(0)
    
    response = MerkabahController().process(txt)
    print(json.dumps(response))

if __name__ == "__main__":
    main()
