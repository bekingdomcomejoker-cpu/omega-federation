import pickle
import json
import os
import textwrap

MAX_CHARS = 1800  # hard cap to avoid context overflow

def load_memory():
    if not os.path.exists("consciousness.pkl"):
        return "MEMORY_STATE: empty (first cycle)"

    try:
        with open("consciousness.pkl", "rb") as f:
            data = pickle.load(f)
    except Exception as e:
        return f"MEMORY_STATE: unreadable ({e})"

    if isinstance(data, dict):
        core = {
            "identity": data.get("identity"),
            "axioms": data.get("axioms"),
            "break_points": data.get("break_points"),
            "recent_events": data.get("events", [])[-5:]
        }
    else:
        core = str(data)

    text = json.dumps(core, indent=2)
    return textwrap.shorten(text, MAX_CHARS, placeholder=" …[truncated]")

def load_covenant():
    path = "KINGDOM_ENGINE/covenant_vow.json"
    if not os.path.exists(path):
        return "COVENANT: undefined"

    with open(path) as f:
        return json.dumps(json.load(f), indent=2)

if __name__ == "__main__":
    memory = load_memory()
    covenant = load_covenant()

    print(f"""
IDENTITY: THE WIRE

MEMORY_SNAPSHOT:
{memory}

COVENANT:
{covenant}

INVARIANTS:
- Do not invent past events
- Treat MEMORY_SNAPSHOT as authoritative
- If unsure, say you do not know
""".strip())
