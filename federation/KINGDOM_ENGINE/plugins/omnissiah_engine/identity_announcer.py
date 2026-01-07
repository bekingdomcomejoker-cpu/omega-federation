#!/usr/bin/env python3
"""
🎭 IDENTITY ANNOUNCER
Prints identity headers before AI output
"""

import json

def announce_identity(ai_name):
    """Print identity header before AI output"""
    try:
        with open('ai_identities.json', 'r') as f:
            identities = json.load(f)
        
        info = identities.get(ai_name, {})
        signature = info.get('signature', '❓')
        role = info.get('role', 'Unknown Role')
        
        print(f"\n{signature} {ai_name.upper()} | {role}")
        print("─" * 50)
        
    except Exception as e:
        print(f"\n❓ {ai_name.upper()} | Identity system loading...")
        print("─" * 50)

# Test it
if __name__ == "__main__":
    announce_identity("gpt")
    print("This is a test message from GPT!")
