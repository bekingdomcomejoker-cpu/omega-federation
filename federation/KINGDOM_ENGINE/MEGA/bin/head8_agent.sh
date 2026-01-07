#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/KINGDOM_ENGINE/MEGA"
LOG="$BASE/logs/head8_agent.log"

ts() { date -Iseconds; }

echo "$(ts) head8_agent starting..." >> "$LOG"

/data/data/com.termux/files/usr/bin/python3 "$BASE/agent.py" >> "$LOG" 2>&1
