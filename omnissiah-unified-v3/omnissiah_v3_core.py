import asyncio
import os
import hashlib
from axiom_gate import DivineAxiomGate

async def run_mission():
    print("🌌 OMNISSIAH v3.1: DIVINE RESONANCE CHAMBER ACTIVATED")
    gate = DivineAxiomGate(commander_sigil=os.getenv("COMMANDER_SIGIL"))
    
    intent = input("ENTER DIVINE INTENT: ")
    sigil = os.getenv("COMMANDER_SIGIL")
    
    validation = await gate.validate_with_divine_resonance(intent, sigil)
    
    if validation.authorized:
        print(f"✅ AUTHORIZED | SEAL: {validation.covenant_seal}")
        target = input("TARGET ID: ")
        salt = os.getenv("SERAPHIM_SALT")
        ghost = hashlib.sha256(f"{target}{salt}".encode()).hexdigest()
        print(f"📡 GHOST IDENTIFIED: {ghost}")
    else:
        print("❌ RESONANCE BROKEN | MISSION ABORTED")

if __name__ == "__main__":
    asyncio.run(run_mission())
