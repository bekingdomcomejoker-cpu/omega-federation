#!/data/data/com.termux/files/usr/bin/bash

LOG=~/KINGDOM_ENGINE/MEGA/logs/heartbeat_status.log

while true; do
    echo "===============================================" > "$LOG"
    echo "   💗  MEGA ENGINE HEARTBEAT (Daemon Mode)" >> "$LOG"
    echo "===============================================" >> "$LOG"
    echo "" >> "$LOG"

    # List heads 1-9
    for h in 1 2 3 4 5 6 7 8 9; do
        PID=$(pgrep -f "head${h}_" | head -n1)
        if [ -n "$PID" ]; then
            echo "🟢 head${h} (PID: $PID)" >> "$LOG"
        else
            echo "⚪ head${h} (NOT RUNNING)" >> "$LOG"
        fi
    done

    echo "" >> "$LOG"
    echo "Updated: $(date --iso-8601=seconds)" >> "$LOG"
    
    sleep 2
done
