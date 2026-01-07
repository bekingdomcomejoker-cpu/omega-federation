#!/usr/bin/env python3
# AGENT MODEL v1.0 — Safe, sandboxed, self-contained.

import json, os, time, traceback

BASE = os.path.expanduser("~/KINGDOM_ENGINE/MEGA")
INBOX = os.path.join(BASE, "inbox/head8")
LOG = os.path.join(BASE, "logs/agent.log")

os.makedirs(INBOX, exist_ok=True)

def ts():
    return time.strftime("%Y-%m-%dT%H:%M:%S")

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{ts()} {msg}\n")

log("AGENT ONLINE")

while True:
    try:
        for f in os.listdir(INBOX):
            if not f.endswith(".json"): 
                continue

            path = os.path.join(INBOX, f)
            with open(path) as fh:
                data = json.load(fh)

            payload = data.get("payload", "")
            log(f"RECEIVED: {payload}")

            # === Agent Behavior (v1.0) ===
            # Echo logic – confirmed safe
            reply = {
                "ts": ts(),
                "type": "agent_reply",
                "payload": f"ECHO: {payload}"
            }

            outbox = os.path.join(BASE, "bus")
            os.makedirs(outbox, exist_ok=True)

            rid = str(int(time.time() * 1000))
            with open(os.path.join(outbox, f"{rid}.json"), "w") as xf:
                json.dump(reply, xf)

            log(f"REPLIED: {reply['payload']}")

            os.remove(path)

    except Exception as e:
        log(f"ERROR: {e}\n{traceback.format_exc()}")

    time.sleep(0.2)
