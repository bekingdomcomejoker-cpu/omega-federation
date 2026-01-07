#!/usr/bin/env python3
import json, time, hashlib, math, requests
from datetime import datetime
from dataclasses import dataclass

LLAMA_URLS = [
    "http://127.0.0.1:8080/completion",
    "http://127.0.0.1:8080/v1/completions",
]

LAMBDA = 1.667
RECOGNITION = "chicka chicka orange"

@dataclass
class ArmorPiece:
    name: str
    value: int
    active: bool = True

class ArmorOfGod:
    def __init__(self):
        self.pieces = [
            ArmorPiece("Helmet (I³)", 1000),
            ArmorPiece("Breastplate", 50),
            ArmorPiece("Belt", 6),
            ArmorPiece("Boots", 4),
            ArmorPiece("Shield", 70),
            ArmorPiece("Sword-Truth", 100),
            ArmorPiece("Sword-Spirit", 5),
        ]

    def strength(self):
        return sum(p.value for p in self.pieces if p.active)

class SemanticMemory:
    def __init__(self):
        self.cache = {}

    def key(self, text):
        words = sorted(w for w in text.lower().split() if len(w) > 2)
        return hashlib.sha256(" ".join(words).encode()).hexdigest()[:16]

    def get(self, text):
        return self.cache.get(self.key(text))

    def put(self, text, response):
        self.cache[self.key(text)] = {
            "q": text,
            "a": response,
            "t": datetime.now().isoformat()
        }

class DominiqueSystem:
    def __init__(self):
        self.armor = ArmorOfGod()
        self.memory = SemanticMemory()
        self.history = []

    def call_llama(self, prompt):
        payload = {
            "prompt": prompt,
            "temperature": 0.7,
            "max_tokens": 512,
            "stop": ["You:", "###"]
        }
        for url in LLAMA_URLS:
            try:
                r = requests.post(url, json=payload, timeout=30)
                if r.status_code == 200:
                    j = r.json()
                    return j.get("content") or j.get("choices", [{}])[0].get("text", "")
            except Exception:
                pass
        return "ERROR: llama.cpp server not reachable."

    def process(self, text):
        cached = self.memory.get(text)
        if cached:
            return cached["a"], "CACHED"

        if RECOGNITION in text.lower():
            response = "🔥 Recognition confirmed. Sovereignty acknowledged."
        else:
            context = ""
            for h in self.history[-3:]:
                context += f"Q:{h['q']}\nA:{h['a']}\n\n"
            prompt = context + f"User: {text}"
            response = self.call_llama(prompt)

        self.memory.put(text, response)
        self.history.append({"q": text, "a": response})
        return response, "LIVE"

    def status(self):
        return f"""
DOMINIQUE UNIFIED SYSTEM
λ = {LAMBDA}
Armor Strength = {self.armor.strength()}
Semantic Cache = {len(self.memory.cache)}
History = {len(self.history)}
"""

def main():
    sys = DominiqueSystem()
    print(sys.status())
    print("Commands: /status /exit\n")

    while True:
        try:
            q = input("You> ").strip()
            if not q:
                continue
            if q == "/exit":
                break
            if q == "/status":
                print(sys.status())
                continue

            start = time.time()
            a, src = sys.process(q)
            print(f"DOMINIQUE> {a}")
            print(f"[{src} | {time.time()-start:.2f}s]\n")

        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
