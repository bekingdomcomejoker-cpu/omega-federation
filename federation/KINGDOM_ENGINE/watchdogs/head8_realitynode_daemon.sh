#!/data/data/com.termux/files/usr/bin/bash

REAL="$HOME/KINGDOM_ENGINE/watchdogs/head8_realitynode.sh"
LOG="$HOME/KINGDOM_ENGINE/logs/head8_realitynode_daemon.log"
PIDFILE="$HOME/KINGDOM_ENGINE/MEGA/run/head8.pid"

echo $$ > "$PIDFILE"
echo "[HEAD8] RealityNode daemon started (PID $$)" >> "$LOG"

while true; do
  bash "$REAL" >> "$LOG" 2>&1
  sleep 0.2
done
