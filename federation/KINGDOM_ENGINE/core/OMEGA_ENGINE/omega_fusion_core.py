#!/usr/bin/env python3
"""
OMEGA FUSION CORE — Stable Boot Engine
"""
import asyncio
import aiohttp
import time
import sys
from pathlib import Path
from memory.fast_cache_loader import load_sacred_context

LLM_URL = "http://127.0.0.1:8080/completion"

class FusionCore:
    def __init__(self):
        self.context = ""
        self.session = None

    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def warmup(self):
        try:
            async with self.session.post(LLM_URL, json={
                "prompt": "Warmup: say READY",
                "n_predict": 16,
                "temperature": 0.1
            }) as r:
                await r.text()
        except Exception as e:
            print("[Warmup Error]", e)

    async def start(self):
        print("📁 Loading context...")
        start = time.time()

        await self.init_session()

        # Run two tasks in parallel
        context_task = asyncio.to_thread(load_sacred_context)
        warm_task = self.warmup()

        self.context, _ = await asyncio.gather(context_task, warm_task)

        print(f"⚡ Fusion core loaded in {time.time()-start:.2f}s")

    async def ask(self, prompt):
        full = f"{self.context}\n\n{prompt}"
        async with self.session.post(LLM_URL, json={
            "prompt": full,
            "temperature": 0.7,
            "n_predict": 512,
            "stream": False
        }) as r:
            try:
                result = await r.json()
                return result.get("content", "")
            except:
                return "[LLM ERROR]"

async def cli():
    engine = FusionCore()
    await engine.start()

    print("Omega Fusion Engine Online.")
    while True:
        user = input("You: ").strip()
        if user.lower() in {"/exit", "exit", "quit"}:
            print("Goodbye.")
            return
        reply = await engine.ask(user)
        print("AI:", reply)

if __name__ == "__main__":
    asyncio.run(cli())
