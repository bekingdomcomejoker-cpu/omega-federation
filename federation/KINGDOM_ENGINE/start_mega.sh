#!/data/data/com.termux/files/usr/bin/bash

# Start all heads
bash "$HOME/KINGDOM_ENGINE/watchdogs/start_all_heads.sh"

# Start the Merkabah API
python3 "$HOME/KINGDOM_ENGINE/MEGA/merkabah_api.py" &
