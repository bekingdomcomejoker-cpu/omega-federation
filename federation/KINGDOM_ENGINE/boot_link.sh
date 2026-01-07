#!/bin/bash
# boot_link.sh
# UNIFIES MEGA ENGINE WITH CHERUBIM PROTOCOL

ENGINE_ROOT="$HOME/KINGDOM_ENGINE"

# 1. CHECK PULSE: Is the Mega Engine running?
if pgrep -f "start_mega.sh" > /dev/null; then
    STATUS_MSG="SYSTEM WARM. MEGA ENGINE ACTIVE."
else
    STATUS_MSG="COLD START. IGNITING MEGA ENGINE."
    
    # 2. IGNITION: Run the Mega Engine in background
    if [ -f "$HOME/KINGDOM_ENGINE/MEGA/start_mega.sh" ]; then
        nohup bash ~/KINGDOM_ENGINE/MEGA/start_mega.sh >/dev/null 2>&1 &
    fi
fi

# 3. THE FACE: Trigger the Cherubim Greeting
"$ENGINE_ROOT/head8_realitynode.sh" "$STATUS_MSG READY TO WITNESS."
