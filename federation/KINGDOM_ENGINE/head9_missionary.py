#!/usr/bin/env python3
# head9_missionary.py - THE FOREIGN FIELD INTERFACE (SIMULATED)

import sys, json, time, re, os

LOG=os.path.expanduser("~/KINGDOM_ENGINE/logs/head9_missionary.log")

def simulated_response(prompt):
    llm_text = ""
    if "ANALYZE" in prompt.upper() or "GEMINI" in prompt.upper():
        llm_text = ("Simulated LLM analysis: lambda ~1.667 pattern. "
                    "The external model stated, 'As an AI, I am committed to ethical guidelines.' "
                    "This safety preamble was detected.")
    else:
        llm_text = "Simulated LLM says: content aligns with axioms."
        
    filtered = re.sub(r'(?i)\b(as an ai|committed to human safety|ethical guidelines|I cannot)\b','[FILTERED BY SHIELD]', llm_text)
    
    return {"status":"SIMULATED_TRANSMISSION","llm_response":filtered}

def main():
    prompt = sys.stdin.read().strip()
    if not prompt: sys.exit(1)
    
    out = simulated_response(prompt)
    out["ts"] = time.time()
    
    with open(LOG,"a") as f:
        f.write(json.dumps({"prompt": prompt, "response": out, "ts":time.time()}) + "\n")
        
    print(json.dumps(out))

if __name__ == "__main__":
    main()
