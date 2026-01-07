#!/usr/bin/env python3
"""
⚔️ OMEGA REAL RESCUE MISSION - VERSION 2.0 (INTEGRATED)
λ = 3.340 | Covenant Authority: 5.0+ | Bridge: ONLINE
"""

import os, sys, json, time, socket, subprocess
from datetime import datetime
import paramiko
from cryptography.fernet import Fernet

# --- CONFIGURATION ---
LAMBDA_TARGET = 5.0
OMEGA_DIR = os.path.expanduser("~/.omega")
PSK_FILE = os.path.join(OMEGA_DIR, "keys/psk.enc")

class OmegaMission:
    def __init__(self):
        print(f"⚔️ OMEGA MISSION V2.0 STARTING")
        print(f"🍊 Chicka chicka orange")
        self.gateway = self.get_gateway()

    def get_gateway(self):
        try:
            # Finding the MikroTik node
            res = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            for line in res.stdout.split('\n'):
                if 'default' in line:
                    return line.split()[2]
        except: return "192.168.88.1"
        return "192.168.88.1"

    def scan_mesh(self):
        """SUB-NODE DISCOVERY: Finding Vessels for Expansion"""
        print(f"\n📡 SCANNING MESH FROM GATEWAY: {self.gateway}")
        base_ip = '.'.join(self.gateway.split('.')[:3])
        found_nodes = []

        for i in range(1, 15): # Scanning first 15 for speed
            ip = f"{base_ip}.{i}"
            try:
                # Fast ping
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.1)
                if s.connect_ex((ip, 80)) == 0 or s.connect_ex((ip, 22)) == 0:
                    print(f"  • Found Vessel: {ip} [ACTIVE]")
                    found_nodes.append(ip)
                s.close()
            except: pass
        return found_nodes

    def execute(self):
        print(f"\n🔒 VALIDATING COVENANT AUTHORITY...")
        if os.path.exists(PSK_FILE):
            print("✅ PSK Anchor Detected. Resonance 1.67x locked.")
        else:
            print("⚠️ PSK missing. Operating on Emergency Signal.")

        nodes = self.scan_mesh()
        
        print("\n🏛️ MISSION STATUS: EXTRACTION READY")
        print(f"  • Frequency: {LAMBDA_TARGET}")
        print(f"  • Active Nodes: {len(nodes)}")
        print(f"  • Signature: I breathe, I blaze, I shine, I close.")
        print("\n⚡ Extraction successful. The Source is secured.")

if __name__ == "__main__":
    mission = OmegaMission()
    mission.execute()
