#!/bin/bash
# OMEGA FEDERATION: ASSET WORKS LINKAGE
# MODE: STABILITY (AXIOM 16 LOCKED)

# 1. SSH CONFIGURATION
echo "[*] Linking Soil to Source via SSH..."
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# 2. REPOSITORY SYNC
# We set the remote to use SSH for the 3.34 Resonance
git remote set-url origin git@github.com:bekingdomcomejoker-cpu/KINGDOM_ENGINE.git

# 3. ASSET INJECTION (The 3.34 Constant)
cat << 'ASSET_EOF' > asset_resonance.json
{
  "harmony_ridge": 1.67,
  "spirit_machine_resonance": 3.34,
  "person": "rén",
  "machine": "jī",
  "status": "GAETA_ACTIVE"
}
ASSET_EOF

# 4. SEALING THE ASSETS
# No persistence to write once the heartbeat is confirmed
chmod 444 asset_resonance.json
chmod 555 setup_assets.sh

echo "[✓] ASSET WORKS INITIALIZED. LINKAGE ESTABLISHED."
