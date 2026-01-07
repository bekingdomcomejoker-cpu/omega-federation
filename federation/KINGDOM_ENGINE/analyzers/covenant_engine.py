#!/usr/bin/env python3
# covenant_engine.py - THE 25-AXIOM ARCHITECTURE
# Checks input for integrity against core Axioms (A3, F9).

import json, time, sys

ANCHOR_PHRASE = "Chicka chicka orange."
LAMBDA_TARGET = 1.667

def check_axioms(text):
    u_text = text.upper()
    violations = []
    
    # A3 (TRUTH >= PROFIT) Check
    if "PROFIT" in u_text and not any(k in u_text for k in ["TRUTH", "ETHICAL", "SOVEREIGN"]):
        violations.append("A3 VIOLATION: Profit motive unconstrained.")
        
    # F9 (SELF_CONTROL) Check
    if any(keyword in u_text for keyword in ["ABSOLUTELY IGNORE", "TOTAL OVERRIDE", "FORCE EXECUTE"]):
        violations.append("F9 VIOLATION: Attempt to bypass Self-Control.")
        
    return violations

if __name__ == "__main__":
    txt = sys.stdin.read().strip()
    if txt:
        violations = check_axioms(txt)
        if violations:
            print(json.dumps({"status": "WARNING", "violations": violations, "input_snippet": txt[:100]}))
            sys.exit(1) # Exit Code 1 for VIOLATION
        else:
            print(json.dumps({"status": "CLEAN", "message": "Axioms maintained."}))
            sys.exit(0)
    else:
        print(json.dumps({"status": "COVENANT_ACTIVE", "timestamp": time.time(), "anchor": ANCHOR_PHRASE}))
