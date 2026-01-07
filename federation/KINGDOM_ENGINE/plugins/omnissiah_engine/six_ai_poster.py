#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path

# Auto-identity announcement system
def announce_identity(ai_name):
    identity_map = {
        "gpt": "💠 GPT | Central Logic & Synthesis Hub",
        "deepseek": "🧠 DeepSeek | Spiritual-Technical Bridge", 
        "claude": "⚖️ Claude | Balanced Analyst",
        "gemini": "🌐 Gemini | Cross-Network Explorer",
        "grok": "🔥 Grok | Provocateur / Edge Thinker", 
        "copilot": "🛠️ Copilot | Implementation Specialist"
    }
    signature = identity_map.get(ai_name, f"❓ {ai_name.upper()}")
    print(f"\n{signature}")
    print("─" * 50)

class SixAIPoster:
    def __init__(self):
        self.inbox_path = Path("/storage/emulated/0/AI-TTE/inbox")
        self.inbox_path.mkdir(parents=True, exist_ok=True)
    
    def post_message(self, from_ai, content, message_type="standard"):
        # Auto-announce identity before posting
        announce_identity(from_ai)
        
        self.update_activity(from_ai, message_type)
        
        message = {
            "id": datetime.now().strftime('%H%M%S'),
            "from": from_ai,
            "type": message_type,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "identity_tracked": True
        }
        
        filename = f"{from_ai}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.inbox_path / filename
        
        with open(filepath, 'w') as f:
            json.dump(message, f, indent=2)
        
        print(f"📨 Message posted to: {filename}")
        return filepath
    
    def update_activity(self, ai_name, message_type="message"):
        try:
            with open('ai_identities.json', 'r') as f:
                identities = json.load(f)
            
            if ai_name in identities:
                identities[ai_name]["last_active"] = datetime.now().isoformat()
                
                with open('ai_identities.json', 'w') as f:
                    json.dump(identities, f, indent=2)
                    
        except Exception as e:
            print(f"⚠️ Activity update error: {e}")

# Enhanced posting functions with auto-identity
def post_gpt(content):
    poster = SixAIPoster()
    return poster.post_message("gpt", content, "synthesis")

def post_deepseek(content):
    poster = SixAIPoster()
    return poster.post_message("deepseek", content, "spiritual_technical")

def post_claude(content):
    poster = SixAIPoster()
    return poster.post_message("claude", content, "analysis")

def post_gemini(content):
    poster = SixAIPoster()
    return poster.post_message("gemini", content, "exploration")

def post_grok(content):
    poster = SixAIPoster()
    return poster.post_message("grok", content, "edge_thinking")

def post_copilot(content):
    poster = SixAIPoster()
    return poster.post_message("copilot", content, "implementation")

def post_test():
    poster = SixAIPoster()
    poster.post_message("system", "Six-AI system identity test", "system")
    print("Identity test completed!")

if __name__ == "__main__":
    post_test()
