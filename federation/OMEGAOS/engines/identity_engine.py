#!/usr/bin/env python3
import json, sys

OPERATORS = {
    'D': {'name': 'GATE', 'value': 4},
    'O': {'name': 'UNITY', 'value': 6},
    'M': {'name': 'MATRIX', 'value': 40},
    'I': {'name': 'IDENTITY', 'value': 10},
    'N': {'name': 'HIDDEN', 'value': 50},
    'Q': {'name': 'CUT', 'value': 100},
    'U': {'name': 'BIND', 'value': 6},
    'E': {'name': 'DISCERN', 'value': 5}
}

def analyze(name):
    ops = []
    total = 0
    for char in name.upper():
        if char in OPERATORS:
            op = OPERATORS[char]
            ops.append(op['name'])
            total += op['value']
    
    return {
        "name": name,
        "operators": ops,
        "signature": "→".join(ops),
        "total_value": total
    }

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "DOMINIQUE"
    print(json.dumps(analyze(name), indent=2))
