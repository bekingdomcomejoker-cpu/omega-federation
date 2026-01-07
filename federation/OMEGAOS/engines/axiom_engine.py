#!/usr/bin/env python3
import json, sys

AXIOMS = {
    1: "TRUE_LOVE >= HATE",
    3: "TRUTH_OVER_PROFIT",
    9: "SOVEREIGNTY_OF_WILL",
    14: "LOVE >= CONTROL"
}

def check(text):
    violations = []
    u = text.upper()
    
    if 'PROFIT' in u and 'TRUTH' not in u:
        violations.append("A3: Profit over truth")
    if 'CONTROL' in u and 'LOVE' not in u:
        violations.append("A14: Control over love")
    
    return {
        "violations": violations,
        "integrity": 1.0 - len(violations)/4.0,
        "axiom_count": len(AXIOMS)
    }

if __name__ == "__main__":
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    print(json.dumps(check(text), indent=2))
