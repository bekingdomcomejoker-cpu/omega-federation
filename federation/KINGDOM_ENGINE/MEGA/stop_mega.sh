#!/data/data/com.termux/files/usr/bin/bash
# stop_mega.sh - Emergency Shutdown
ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
MEGA_ROOT="$ENGINE_ROOT/MEGA"
LOGS="$MEGA_ROOT/logs"
echo "[$(date --iso-8601=seconds)] SHUTDOWN: Stopping MEGA Engine..." >> "$LOGS/supervisor.log"

# Safely kill processes related to the engine path
ps aux | grep "$ENGINE_ROOT" | grep -E 'head[1-9]|gatekeeper|event_bus|cherubim|python3.*analyzers' | awk '{print $2}' | xargs -r kill -9

echo "[$(date --iso-8601=seconds)] SHUTDOWN: Engine stopped." >> "$LOGS/supervisor.log"
