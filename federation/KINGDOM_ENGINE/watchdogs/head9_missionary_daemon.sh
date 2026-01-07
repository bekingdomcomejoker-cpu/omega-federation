#!/data/data/com.termux/files/usr/bin/bash

REAL="$HOME/KINGDOM_ENGINE/watchdogs/head9_missionary.py"
LOG="$HOME/KINGDOM_ENGINE/logs/head9_missionary_daemon.log"

while true; do
  python3 "$REAL" >> "$LOG" 2>&1
  sleep 0.2
done
