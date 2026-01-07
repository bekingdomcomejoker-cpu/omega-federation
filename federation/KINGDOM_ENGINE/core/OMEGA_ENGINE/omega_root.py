#!/usr/bin/env python3
"""
OMEGA Unified Engine - Async + Fusion + Fast Boot
Full replacement file (A + B + C integrated).
"""
import os, sys, asyncio, time, signal
from pathlib import Path
import aiohttp

HOME = Path(os.environ.get("HOME", "/data/data/com.termux/files/home"))
LLAMA_MODEL = os.environ.get("LLAMA_MODEL_PATH",
    str(HOME / "KINGDOM_ENGINE" / "models" / "llama_cpp" / "models" / "tinyllama.gguf"))
LOCAL_LLM_URL = os.environ.get("LOCAL_LLM_URL", "http://127.0.0.1:8080/completion")

MEMORY_DIR = HOME / "KINGDOM_ENGINE" / "memory"

try:
    from KINGDOM_ENGINE.memory.fast_cache_loader import load_sacred_context
except Exception:
    sys.path.insert(0, str(HOME / "KINGDOM_ENGINE"))
    try:
        from memory.fast_cache_loader import load_sacred_context
    except:
        load_sacred_context = lambda: ""

try:
    from KINGDOM_ENGINE.core.OMEGA_ENGINE.multi_ai import MultiAI
except:
    try:
        from multi_ai import MultiAI
    except:
        MultiAI = None

multi_ai = MultiAI() if MultiAI else None
_shared_session = None

async def ensure_session():
    global _shared_session
    if _shared_session is None:
        _shared_session = aiohttp.ClientSession()
    return _shared_session

async def warmup_llm():
    try:
        session = await ensure_session()
        payload = {"prompt": "<s> Hello, respond READY", "n_predict": 16, "temperature": 0.1}
        async with session.post(LOCAL_LLM_URL, json=payload, timeout=10) as resp:
            await resp.text()
            print("[OMEGA] LLM warmed up")
            return True
    except Exception as e:
        print("[OMEGA] Warmup LLM failed:", e)
        return False

async def start_llama_if_missing():
    import shutil, subprocess, requests
    if shutil.which("llama-server") is None:
        return False

    try:
        try:
            r = requests.get(LOCAL_LLM_URL.replace("/completion", "/health"), timeout=2)
            if r.status_code == 200:
                return True
        except:
            pass

        cwd = HOME / "KINGDOM_ENGINE" / "models" / "llama_cpp"
        cmd = [
            str(cwd / "llama-server"),
            "-m", LLAMA_MODEL,
            "--host", "127.0.0.1",
            "--port", "8080",
            "-t", "4",
            "-c", "2048"
        ]

        print("[OMEGA] Starting llama-server…")
        subprocess.Popen(cmd, cwd=str(cwd),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        import requests
        for _ in range(15):
            try:
                r = requests.get(LOCAL_LLM_URL.replace("/completion", "/health"), timeout=2)
                if r.status_code == 200:
                    print("[OMEGA] llama-server ready")
                    return True
            except:
                await asyncio.sleep(0.5)

        print("[OMEGA] llama-server did not start in time.")
        return False
    except Exception as e:
        print("[OMEGA] Failed to start llama-server:", e)
        return False

async def load_context_incremental():
    try:
        ctx = load_sacred_context()
        print("[OMEGA] Loaded sacred context (len=%d)" % len(ctx))
        return ctx
    except Exception as e:
        print("[OMEGA] load_context failed:", e)
        return ""

async def ask_local_llm(prompt: str, n_predict=256, temp=0.7):
    try:
        session = await ensure_session()
        payload = {"prompt": prompt, "n_predict": n_predict, "temperature": temp}
        async with session.post(LOCAL_LLM_URL, json=payload, timeout=60) as resp:
            try:
                data = await resp.json()
                if isinstance(data, dict):
                    for k in ("content","text","output"):
                        if k in data:
                            return data[k]
                    if "choices" in data and data["choices"]:
                        return data["choices"][0].get("text") or str(data)
                return str(data)
            except:
                return await resp.text()
    except Exception as e:
        return f"[LLM ERROR] {e}"

async def ask(prompt: str, persona: str = "local"):
    if multi_ai:
        try:
            return await multi_ai.ask(persona, prompt)
        except Exception as e:
            print("[OMEGA] multi_ai.ask failed:", e)
    return await ask_local_llm(prompt)

def print_help():
    print("""[OMEGA] Commands:
/help
/quit
/restart_llm
/health
/cache_reload
/personas
""")

async def interactive_loop():
    ctx = await load_context_incremental()
    await asyncio.gather(start_llama_if_missing(), warmup_llm())
    print("[OMEGA] Omega Root Engine CLI. Type /help.")

    while True:
        try:
            prompt = await asyncio.to_thread(input, "You: ")
        except:
            print("\n[OMEGA] Exiting.")
            break

        if not prompt:
            continue
        if prompt.strip() in ("/quit","quit","exit"):
            break
        if prompt.strip() == "/help":
            print_help(); continue
        if prompt.strip() == "/restart_llm":
            await start_llama_if_missing(); continue
        if prompt.strip() == "/
