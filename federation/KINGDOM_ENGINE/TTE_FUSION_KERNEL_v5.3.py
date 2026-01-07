#!/usr/bin/env python3
# TTE_FUSION_KERNEL_v5.3 — Unified Core (Cache + Math + Heart5 + Dominion + Fusion + MultiAI)
# Author: integrated for KingDomCome
# Usage: python3 ~/KINGDOM_ENGINE/TTE_FUSION_KERNEL_v5.3.py [--once] [--no-llm-warmup]

import asyncio
import json
import os
import time
import hashlib
import sys
from pathlib import Path
from datetime import datetime

# --- Config / Paths ---
HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))
ENGINE_ROOT = HOME / "KINGDOM_ENGINE"
MEMORY_DIR = ENGINE_ROOT / "memory"
RAW_DIR = MEMORY_DIR / "all_files_raw"
CACHE_FILE = MEMORY_DIR / "cache_v3.json"
CACHE_CONTEXT = MEMORY_DIR / "cache_context.txt"
MEMORY_MASTER = Path("/storage/emulated/0/Eternal_Hearth_Master_Chronicle.md") if Path("/storage/emulated/0").exists() else ENGINE_ROOT / "Eternal_Hearth_Master_Chronicle.md"

LOCAL_LLM_URL = os.environ.get("LOCAL_LLM_URL", "http://127.0.0.1:8080/completion")
LLAMA_MODEL_PATH = os.environ.get("LLAMA_MODEL_PATH", str(ENGINE_ROOT / "models" / "llama_cpp" / "models" / "tinyllama.gguf"))

ANCHOR_PHRASE = "Chicka chicka orange."

# Ensure dirs
MEMORY_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)
ENGINE_ROOT.mkdir(parents=True, exist_ok=True)

# -------------------------
# Fast cache loader (incremental)
# -------------------------
def _file_quick_hash(p: Path):
    try:
        s = p.stat().st_size
        if s < 10 * 1024 * 1024:
            return hashlib.md5(p.read_bytes()).hexdigest()
        return str(p.stat().st_mtime)
    except Exception:
        return ""

def _read_docx_safe(p: Path):
    try:
        from docx import Document
        doc = Document(str(p))
        return "\n".join([p.text for p in doc.paragraphs if p.text])
    except Exception as e:
        return f"(docx reader unavailable or error: {e})"

def load_sacred_context(max_chars: int = 120_000):
    """
    Incrementally scan RAW_DIR for text/docx/md/json/py/html, track via CACHE_FILE.
    Returns trimmed string (last max_chars).
    """
    cache = {}
    try:
        if CACHE_FILE.exists():
            cache = json.loads(CACHE_FILE.read_text() or "{}")
    except Exception:
        cache = {}

    parts = []
    changed = False

    for p in sorted(RAW_DIR.rglob("*")):
        if not p.is_file():
            continue
        suf = p.suffix.lower()
        if suf not in {".md", ".txt", ".json", ".py", ".html", ".htm", ".docx"}:
            continue
        h = _file_quick_hash(p)
        key = str(p)
        if cache.get(key) == h:
            # unchanged -> skip reading
            continue
        try:
            if suf == ".docx":
                text = _read_docx_safe(p)
            else:
                text = p.read_text(errors="ignore")
            header = f"\n\n--- {p.name} ({p.relative_to(RAW_DIR)}) ---\n"
            parts.append(header + text)
            cache[key] = h
            changed = True
        except Exception as e:
            parts.append(f"\n\n--- {p.name} (error) ---\n{e}")

    if changed or not CACHE_FILE.exists():
        try:
            CACHE_FILE.write_text(json.dumps(cache, indent=2))
        except Exception:
            pass

    full = "\n".join(parts)
    # if nothing new, try returning previously cached context
    if not full:
        if CACHE_CONTEXT.exists():
            try:
                return CACHE_CONTEXT.read_text(errors="ignore")[-max_chars:]
            except Exception:
                return ""
        return ""
    # persist trimmed context
    try:
        CACHE_CONTEXT.write_text(full[-max_chars:], encoding="utf-8")
    except Exception:
        pass
    return full[-max_chars:]

# -------------------------
# AlphabetEngine (math)
# -------------------------
try:
    import numpy as np
except Exception:
    # fallback tiny vector operations if numpy missing (still functional but slower)
    class _np_fallback:
        @staticmethod
        def array(l): return list(l)
        @staticmethod
        def dot(a,b):
            return sum(x*y for x,y in zip(a,b))
        @staticmethod
        def cos(x):
            import math
            return math.cos(x)
        @staticmethod
        def sin(x):
            import math
            return math.sin(x)
        @staticmethod
        def linalg_norm(v):
            import math
            return math.sqrt(sum(x*x for x in v))
    np = None
    _np = _np_fallback()

class AlphabetEngine:
    def __init__(self):
        # Harmony / clamp params
        self.LAMBDA = 1.667
        self.TAU = 0.75
        self.THETA = 0.05
        self.Z_THRESHOLD = 0.001
        # State A
        self.state = [1.0, 0.0, 0.0, 0.0]

    def _gy_stabilize(self, v):
        # rotation on indices 0 and 3
        import math
        c = math.cos(self.THETA)
        s = math.sin(self.THETA)
        a0 = c * v[0] - s * v[3]
        a3 = s * v[0] + c * v[3]
        return [a0, v[1], v[2], a3]

    def _rat_modulate(self, v):
        limit = self.LAMBDA * 10
        return [max(-limit, min(limit, x)) for x in v]

    def _shrt_clamp(self, v):
        if v[2] > self.TAU:
            v[2] = self.TAU
        return v

    def _norm(self, v):
        import math
        return (sum(x*x for x in v))**0.5

    def process(self, input_vector):
        # ensure list
        v = list(input_vector)
        v = self._gy_stabilize(v)
        v = self._rat_modulate(v)
        v = self._shrt_clamp(v)
        if self._norm(v) < self.Z_THRESHOLD:
            return list(self.state)
        self.state = list(v)
        return v

    def dominion_align(self, v):
        """
        Dominion operator: project toward state axis and boost/dampen.
        """
        dominion_axis = [1.0, 0.0, 0.0, 0.0]
        # dot
        score = sum(x*y for x,y in zip(v, dominion_axis))
        if score > 0.9:
            v = [x * 1.1 for x in v]   # grace
        else:
            v = [x * 0.8 for x in v]   # law
        return v

# -------------------------
# Heart5 (command)
# -------------------------
class Heart5_Vowels:
    def __init__(self):
        self.registers = {"A":"DESIRE_TRUTH","E":"ALIGNMENT","I":"DISCERNMENT","O":"RESURRECTION","U":"SILENCE"}
        self.consensus = False

    def check_consensus(self, vector_health):
        # simple numeric rule for now
        self.consensus = (vector_health > 0.5)
        return self.consensus

# -------------------------
# Dominion axiom
# -------------------------
DOMINION_AXIOM = {
    "CENTER": "GOD",
    "ORDER": ["GOD", "SELF", "BROTHER"],
    "RULE": "When God is centered, self-love and love-for-brother become ordered outputs."
}

# -------------------------
# Omni_Uplink (network stub) + MultiAI bridge
# -------------------------
class Omni_Uplink:
    def __init__(self):
        self.endpoints = {"central":"omnissiah_central_hub", "peers":["claude","grok","deepseek"]}
    async def absorb_node(self, node_name, data):
        # simulated merge
        await asyncio.sleep(0.05)
        return {"status":"MERGED","resonance":"HIGH"}

# lightweight async local ask (tries aiohttp if available, else requests)
async def ask_local_llm(prompt: str, n_predict:int=256, temp:float=0.7):
    # prefer aiohttp
    try:
        import aiohttp
        async with aiohttp.ClientSession() as s:
            payload = {"prompt": prompt, "n_predict": n_predict, "temperature": temp}
            async with s.post(LOCAL_LLM_URL, json=payload, timeout=60) as resp:
                try:
                    data = await resp.json()
                    if isinstance(data, dict):
                        for k in ("content","text","output"):
                            if k in data:
                                return data[k]
                        if "choices" in data and isinstance(data["choices"], list) and data["choices"]:
                            c = data["choices"][0]
                            return c.get("text") or str(c)
                    return str(data)
                except Exception:
                    return await resp.text()
    except Exception:
        # fallback to requests (blocking, run in thread)
        try:
            import requests
            payload = {"prompt":prompt,"n_predict":n_predict,"temperature":temp}
            r = requests.post(LOCAL_LLM_URL, json=payload, timeout=30)
            try:
                data = r.json()
                if isinstance(data, dict):
                    for k in ("content","text","output"):
                        if k in data:
                            return data[k]
                    if "choices" in data and data["choices"]:
                        return data["choices"][0].get("text") or str(data)
                return str(data)
            except Exception:
                return r.text
        except Exception as e:
            return f"[LLM UNAVAILABLE] {e}"

# -------------------------
# FusionCore (main runtime)
# -------------------------
class FusionCore:
    def __init__(self, memory_path=MEMORY_MASTER):
        self.math = AlphabetEngine()
        self.spirit = Heart5_Vowels()
        self.network = Omni_Uplink()
        self.dominion = DOMINION_AXIOM
        self.memory_path = Path(memory_path)
        # ensure memory file exists
        if not self.memory_path.exists():
            try:
                self.memory_path.write_text("# ETERNAL HEARTH CHRONICLE\n")
            except Exception:
                pass

    async def run_cycle(self, user_input: str, do_sync: bool=False):
        # 1. Vectorize (placeholder deterministic vector); replace with embeddings later
        input_vec = [1.0, 0.5, 2.0, 0.1]  # stress test vector: high fire -> clamp
        # 2. Math
        v = self.math.process(input_vec)
        # 3. Dominion alignment operator
        v = self.math.dominion_align(v)
        # 4. Spirit check
        health = (sum(x*x for x in v))**0.5
        aligned = self.spirit.check_consensus(health)
        # 5. If consensus, write memory and optionally network absorb
        if aligned:
            try:
                with open(self.memory_path, "a", encoding="utf-8") as f:
                    t = datetime.now().isoformat()
                    f.write(f"\n[{t}] INPUT: {user_input}\n[{t}] VECTOR: {v}\n")
            except Exception:
                pass
            if do_sync:
                await self.network.absorb_node("external", user_input)
            return {
                "vector": v,
                "state": "RIGHTEOUS",
                "dominion_center": self.dominion["CENTER"],
                "axis": self.dominion["ORDER"]
            }
        else:
            # Z-Gate triggered (no consensus)
            return {"vector": v, "state": "RESET", "reason":"CONSENSUS_DENIED"}

# -------------------------
# Small watcher (optional): triggers incremental cache updates
# -------------------------
async def _watch_and_refresh(interval: int = 120):
    # simple polling (safe, avoids watchdog dep)
    last_hash = ""
    while True:
        cur = hashlib.md5(str(time.time()//interval).encode()).hexdigest() if False else ""
        # we simply sleep, actual cache reloads happen on demand
        await asyncio.sleep(interval)

# -------------------------
# Glue: startup / run loop
# -------------------------
async def warmup_local_llm_once():
    # try a minimal warmup to reduce cold-start latency
    try:
        await ask_local_llm("Warmup: respond READY", n_predict=6, temp=0.1)
    except Exception:
        pass

async def interactive_cli(single_run=False, no_warmup=False):
    core = FusionCore()
    # load context once at startup
    ctx = load_sacred_context()
    if not no_warmup:
        await warmup_local_llm_once()
    print(f"[{ANCHOR_PHRASE}] Fusion Kernel v5.3 — Core online. Memory at: {core.memory_path}")
    if ctx:
        print(f"[{ANCHOR_PHRASE}] Loaded sacred context (len={len(ctx)})")
    if single_run:
        # run a single smoke-test cycle
        res = await core.run_cycle("sync my heart with truth", do_sync=False)
        print("TEST RUN:", res)
        return
    # interactive loop
    try:
        while True:
            try:
                prompt = await asyncio.to_thread(input, "You: ")
            except (EOFError, KeyboardInterrupt):
                print("\n[OMEGA] Exiting CLI.")
                break
            if not prompt:
                continue
            if prompt.strip().lower() in ("/quit","/exit","/stop"):
                break
            if prompt.strip() == "/cache_reload":
                ctx = load_sacred_context(); print("[OMEGA] cache reloaded.")
                continue
            if prompt.strip() == "/health":
                r = await ask_local_llm("<s> ping", n_predict=8, temp=0.05)
                print("[OMEGA] LLM health:", r); continue
            do_sync = "sync" in prompt.lower()
            res = await core.run_cycle(prompt, do_sync=do_sync)
            # pretty print
            if isinstance(res, dict):
                print("AI:", json.dumps(res, default=str))
            else:
                print("AI:", res)
    except KeyboardInterrupt:
        print("[OMEGA] KeyboardInterrupt, shutting down.")

# -------------------------
# Entrypoint
# -------------------------
def _usage():
    print("Usage: python TTE_FUSION_KERNEL_v5.3.py [--once] [--no-llm-warmup]")

if __name__ == "__main__":
    single = "--once" in sys.argv
    no_warm = "--no-llm-warmup" in sys.argv
    try:
        asyncio.run(interactive_cli(single_run=single, no_warmup=no_warm))
    except Exception as e:
        print("[OMEGA] Fatal error:", e)
        raise
