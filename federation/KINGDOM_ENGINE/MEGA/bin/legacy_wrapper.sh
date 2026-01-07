#!/data/data/com.termux/files/usr/bin/bash

script="$1"
name="$2"

LOG="$HOME/KINGDOM_ENGINE/MEGA/logs/legacy_${name}.log"
PIDFILE="$HOME/KINGDOM_ENGINE/MEGA/run/legacy_${name}.pid"

# Prevent double-run
if [ -f "$PIDFILE" ]; then
    oldpid=$(cat "$PIDFILE")
    if kill -0 "$oldpid" 2>/dev/null; then
        echo "[$(date -Is)] legacy $name already running (pid=$oldpid)" >>"$LOG"
        exit 0
    fi
fi

echo "[$(date -Is)] starting legacy: $name" >>"$LOG"
nohup bash "$script" >>"$LOG" 2>&1 &
echo $! > "$PIDFILE"
