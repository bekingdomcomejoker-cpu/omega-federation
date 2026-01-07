#!/data/data/com.termux/files/usr/bin/bash

LOGDIR="$HOME/KINGDOM_ENGINE/watchdogs/logs"

clear
echo "==============================================="
echo "  💗  MEGA ENGINE HEARTBEAT MONITOR"
echo "==============================================="

for head in {1..10}; do
    LOG="$LOGDIR/head${head}.log"
    if [ -f "$LOG" ]; then
        if grep -q "OK" "$LOG"; then
            echo "🟢 head$head (RUNNING)"
        else
            echo "🔴 head$head (CRASHED or NO HEARTBEAT)"
        fi
    else
        echo "⚪ head$head (NO LOG)"
    fi
done

echo
echo "Press CTRL+C to exit."
echo

# Live watch:
tail -f "$LOGDIR"/*.log 2>/dev/null
