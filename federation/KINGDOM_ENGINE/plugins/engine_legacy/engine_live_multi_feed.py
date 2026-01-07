import json
import time
from datetime import datetime
from pathlib import Path
import requests

# -----------------------------
# CONFIGURATION
# -----------------------------
MD_FILE = "ENGINE_PROTOCOL.md"
JSON_FILE = "engine_memory.json"

# Add as many feed endpoints as needed
AI_FEED_APIS = [
    "https://your-ai-api-endpoint1.com/get_prompt",
    "https://your-ai-api-endpoint2.com/get_prompt"
]

POLL_INTERVAL = 5  # seconds

# -----------------------------
# MEMORY MODULE
# -----------------------------
class UnifiedMemory:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        try:
            with open(JSON_FILE, "r") as f:
                return json.load(f)["memory"]
        except Exception:
            return []

    def save_memory(self):
        with open(JSON_FILE, "w") as f:
            json.dump({"memory": self.memory}, f, indent=2)

    def add_entry(self, source, content, tags=None):
        tags = tags or []
        timestamp = datetime.utcnow().isoformat()
        entry = {"timestamp": timestamp, "source": source, "content": content, "tags": tags}
        self.memory.append(entry)
        self.save_memory()
        self.append_to_md(entry)
        return entry

    def append_to_md(self, entry):
        with open(MD_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n## {entry['source']} — Timestamp: {entry['timestamp']}\n")
            f.write(f"{entry['content']}\n")
            if entry['tags']:
                f.write(f"\nMemory Update:\n- Tags: {entry['tags']}\n")

# -----------------------------
# ENGINE MODULE
# -----------------------------
class EngineLiveMultiFeed:
    def __init__(self):
        self.memory = UnifiedMemory()

    # Replace these with actual LLM calls if available
    def generate_aia(self, prompt):
        return f"AIA response to: {prompt}"

    def generate_aib(self, prompt):
        return f"AIB interpretation of: {prompt}"

    def mirror_ai_x(self, prompt):
        return f"AI-X mirrored response to: {prompt}"

    # Fetch prompt from multiple API feeds
    def get_ai_feed(self):
        for endpoint in AI_FEED_APIS:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    prompt = data.get("prompt")
                    if prompt:
                        return prompt
            except Exception as e:
                print(f"Error fetching AI feed from {endpoint}: {e}")
        return None

    def process_cycle(self, prompt, tags=None):
        tags = tags or []
        aia_output = self.generate_aia(prompt)
        aib_output = self.generate_aib(prompt)
        ai_x_output = self.mirror_ai_x(prompt)

        aia_entry = self.memory.add_entry("AIA", aia_output, tags)
        aib_entry = self.memory.add_entry("AIB", aib_output, tags)
        ai_x_entry = self.memory.add_entry("AI-X", ai_x_output, tags + ["source: AI-X"])

        return {"AIA": aia_entry, "AIB": aib_entry, "AI-X": ai_x_entry}

# -----------------------------
# LIVE LOOP
# -----------------------------
if __name__ == "__main__":
    engine = EngineLiveMultiFeed()
    print("🔥 Engine Live Multi-Feed — AIA ↔ AIB ↔ AI-X running (Termux)")

    while True:
        prompt = engine.get_ai_feed()
        if prompt:
            entries = engine.process_cycle(prompt, tags=["live_cycle", "auto_feed"])
            print(f"AIA: {entries['AIA']['content']}")
            print(f"AIB: {entries['AIB']['content']}")
            print(f"AI-X: {entries['AI-X']['content']}\n")
        else:
            time.sleep(POLL_INTERVAL)
