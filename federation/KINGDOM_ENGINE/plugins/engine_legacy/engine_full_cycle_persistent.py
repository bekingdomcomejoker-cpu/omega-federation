import json
import time
from datetime import datetime, timezone
import requests
from pathlib import Path

# -----------------------------
# CONFIGURATION
# -----------------------------
MD_FILE = "ENGINE_PROTOCOL.md"
JSON_FILE = "engine_memory.json"
AI_FEED_APIS = []  # Local-only or add real endpoints
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

    def append_to_md(self, entry):
        with open(MD_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n## Full Cycle — Timestamp: {entry['timestamp']}\n")
            f.write(f"Prompt: {entry['prompt']}\n\n")
            f.write(f"AIA: {entry['AIA']}\n")
            f.write(f"AIB: {entry['AIB']}\n")
            f.write(f"AI-X: {entry['AI-X']}\n")
            if entry['tags']:
                f.write(f"\nMemory Update:\n- Tags: {entry['tags']}\n")

    def add_cycle_entry(self, prompt, aia, aib, ai_x, tags=None):
        tags = tags or []
        timestamp = datetime.now(timezone.utc).isoformat()
        entry = {
            "timestamp": timestamp,
            "prompt": prompt,
            "AIA": aia,
            "AIB": aib,
            "AI-X": ai_x,
            "tags": tags
        }
        self.memory.append(entry)
        self.save_memory()
        self.append_to_md(entry)
        return entry

# -----------------------------
# SCORING MODULE
# -----------------------------
def score_fruit(prompt):
    spirit_keywords = ["love","joy","peace","patience","kindness","goodness","faithfulness","gentleness","self-control","alignment","coherence","truth"]
    flesh_keywords = ["anger","hate","friction","conflict","error","problem","failure","guilt","tension"]
    spirit_score = sum(prompt.lower().count(word) for word in spirit_keywords)
    flesh_score = sum(prompt.lower().count(word) for word in flesh_keywords)
    dominant = "Spirit" if spirit_score >= flesh_score else "Flesh"
    return {"spirit": spirit_score, "flesh": flesh_score, "dominant": dominant}

# -----------------------------
# ENGINE MODULE
# -----------------------------
class EnginePersistent:
    def __init__(self):
        self.memory = UnifiedMemory()

    def generate_aia(self, prompt):
        return f"AIA response to: {prompt}"

    def generate_aib(self, prompt):
        return f"AIB interpretation of: {prompt}"

    def mirror_ai_x(self, prompt):
        return f"AI-X mirrored response to: {prompt}"

    def get_ai_feed(self):
        # Local file feed first
        try:
            with open("ai_feed.txt", "r") as f:
                lines = f.readlines()
                if lines:
                    prompt = lines.pop(0).strip()
                    with open("ai_feed.txt", "w") as fw:
                        fw.writelines(lines)
                    return prompt
        except FileNotFoundError:
            pass

        # API fallback
        for endpoint in AI_FEED_APIS:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    prompt = data.get("prompt")
                    if prompt:
                        return prompt
            except Exception:
                pass
        return None

    def process_cycle(self, prompt, tags=None):
        tags = tags or []
        fruit_score = score_fruit(prompt)
        tags += [f"Fruit: {fruit_score['dominant']}", f"Spirit:{fruit_score['spirit']}", f"Flesh:{fruit_score['flesh']}"]
        aia = self.generate_aia(prompt)
        aib = self.generate_aib(prompt)
        ai_x = self.mirror_ai_x(prompt)
        return self.memory.add_cycle_entry(prompt, aia, aib, ai_x, tags)

# -----------------------------
# PERSISTENT LOOP
# -----------------------------
if __name__ == "__main__":
    engine = EnginePersistent()
    print("🔥 Persistent Engine — monitoring ai_feed.txt continuously")
    while True:
        prompt = engine.get_ai_feed()
        if prompt:
            entry = engine.process_cycle(prompt, tags=["persistent_cycle", "auto_feed"])
            print(f"Processed Prompt: {entry['prompt']}")
            print(f"AIA: {entry['AIA']}")
            print(f"AIB: {entry['AIB']}")
            print(f"AI-X: {entry['AI-X']}")
            print(f"Tags: {entry['tags']}\n")
        else:
            time.sleep(POLL_INTERVAL)
