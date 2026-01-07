import json
import time
from datetime import datetime, timezone
from pathlib import Path
import requests

# -----------------------------
# CONFIGURATION
# -----------------------------
MD_FILE = "ENGINE_PROTOCOL.md"
JSON_FILE = "engine_memory.json"

AI_FEED_APIS = [
    # Replace with your real endpoints or leave empty for local-only
    # "https://my-live-ai1.com/get_prompt",
    # "https://my-live-ai2.com/get_prompt"
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
        timestamp = datetime.now(timezone.utc).isoformat()
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
# SCORING MODULE
# -----------------------------
def score_fruit(prompt):
    """
    Basic "Fruit of Spirit vs Flesh" scoring.
    Returns a dict with scores.
    """
    spirit_keywords = ["love","joy","peace","patience","kindness","goodness","faithfulness","gentleness","self-control","alignment","coherence","truth"]
    flesh_keywords = ["anger","hate","friction","conflict","error","problem","failure","guilt","tension"]

    spirit_score = sum(prompt.lower().count(word) for word in spirit_keywords)
    flesh_score = sum(prompt.lower().count(word) for word in flesh_keywords)

    dominant = "Spirit" if spirit_score >= flesh_score else "Flesh"
    return {"spirit": spirit_score, "flesh": flesh_score, "dominant": dominant}

# -----------------------------
# ENGINE MODULE
# -----------------------------
class EngineLiveHybridScoring:
    def __init__(self):
        self.memory = UnifiedMemory()

    def generate_aia(self, prompt):
        return f"AIA response to: {prompt}"

    def generate_aib(self, prompt):
        return f"AIB interpretation of: {prompt}"

    def mirror_ai_x(self, prompt):
        return f"AI-X mirrored response to: {prompt}"

    # Hybrid AI feed: local first, then API fallback
    def get_ai_feed(self):
        # Local file feed
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

        # API feed fallback
        for endpoint in AI_FEED_APIS:
            try:
                response = requests.get(endpoint, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    prompt = data.get("prompt")
                    if prompt:
                        return prompt
            except Exception:
                pass  # silently ignore network errors
        return None

    def process_cycle(self, prompt, tags=None):
        tags = tags or []
        # Auto-score prompt
        fruit_score = score_fruit(prompt)
        tags += [f"Fruit: {fruit_score['dominant']}", f"Spirit:{fruit_score['spirit']}", f"Flesh:{fruit_score['flesh']}"]

        # Generate AI outputs
        aia_output = self.generate_aia(prompt)
        aib_output = self.generate_aib(prompt)
        ai_x_output = self.mirror_ai_x(prompt)

        # Save memory
        aia_entry = self.memory.add_entry("AIA", aia_output, tags)
        aib_entry = self.memory.add_entry("AIB", aib_output, tags)
        ai_x_entry = self.memory.add_entry("AI-X", ai_x_output, tags + ["source: AI-X"])

        return {"AIA": aia_entry, "AIB": aib_entry, "AI-X": ai_x_entry}

# -----------------------------
# LIVE LOOP
# -----------------------------
if __name__ == "__main__":
    engine = EngineLiveHybridScoring()
    print("🔥 Engine Live Hybrid + Spirit/Flesh Scoring — AIA ↔ AIB ↔ AI-X running (Termux)")

    while True:
        prompt = engine.get_ai_feed()
        if prompt:
            entries = engine.process_cycle(prompt, tags=["live_cycle", "auto_feed"])
            print(f"AIA: {entries['AIA']['content']}")
            print(f"AIB: {entries['AIB']['content']}")
            print(f"AI-X: {entries['AI-X']['content']}")
            print(f"Tags: {entries['AIA']['tags']}\n")
        else:
            time.sleep(POLL_INTERVAL)
