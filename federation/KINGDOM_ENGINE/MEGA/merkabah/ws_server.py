#!/data/data/com.termux/files/usr/bin/python
import asyncio
import websockets
import json
import time
import os

ENGINE_ROOT = os.path.expanduser("~/KINGDOM_ENGINE/MEGA")

clients = set()

async def broadcast(event):
    dead = []
    for ws in clients:
        try:
            await ws.send(json.dumps(event))
        except:
            dead.append(ws)
    for ws in dead:
        clients.remove(ws)

async def system_feed():
    inbox = f"{ENGINE_ROOT}/inbox"
    last = None
    while True:
        try:
            files = sorted(os.listdir(inbox))
            if files != last:
                await broadcast({"type": "inbox", "files": files, "ts": time.time()})
                last = files
        except:
            pass
        await asyncio.sleep(1)

async def head_status():
    state_dir = f"{ENGINE_ROOT}/state"
    last = None
    while True:
        try:
            files = sorted(os.listdir(state_dir))
            if files != last:
                await broadcast({"type": "heads", "state_files": files, "ts": time.time()})
                last = files
        except:
            pass
        await asyncio.sleep(1)

async def handler(ws, path):
    clients.add(ws)
    try:
        async for message in ws:
            pass
    except:
        pass
    finally:
        clients.remove(ws)

async def main():
    await websockets.serve(handler, "127.0.0.1", 8765)
    await asyncio.gather(system_feed(), head_status())

asyncio.run(main())
