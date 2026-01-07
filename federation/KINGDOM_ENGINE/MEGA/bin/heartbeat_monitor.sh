#!/data/data/com.termux/files/usr/bin/bash

ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
PIDS="$ENGINE_ROOT/MEGA/run"
LOGS="$ENGINE_ROOT/MEGA/logs"

while true; do
    clear
    echo "============================================="
    echo "       💓 MEGA ENGINE HEARTBEAT MONITOR"
    echo "============================================="
    echo ""
    
    # HEAD STATUS
    echo "🧠 HEAD STATUS:"
    for head in head1 head2 head3 head4 head5 head6 head7 head8 head9; do
        PID_FILE="$PIDS/${head}.pid"
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if ps -p "$PID" > /dev/null 2>&1; then
                echo "  🟢 $head (PID: $PID)"
            else
                echo "  🔴 $head (CRASHED)"
            fi
        else
            echo "  ⚪ $head (NOT STARTED)"
        fi
    done
    
    echo ""
    echo "📡 LAST ROUTER ACTION:"
    tail -n 3 "$LOGS/gatekeeper.log" 2>/dev/null
    
    echo ""
    echo "👁️ LAST CHERUBIM FACE:"
    tail -n 3 "$LOGS/cherubim.log" 2>/dev/null

    echo ""
    echo "🛡️ LAST SHIELD BLOCK:"
    grep -i QUARANTINE "$LOGS/gatekeeper.log" | tail -n 3 2>/dev/null
    
    echo ""
    echo "⚔️ LAST SWORD ACTION:"
    grep -i EXECUTE "$LOGS/gatekeeper.log" | tail -n 3 2>/dev/null

    echo ""
    echo "📥 LATEST INBOX EVENTS (HEAD 1):"
    ls -1t "$ENGINE_ROOT/MEGA/inbox/head1" 2>/dev/null | head -n 5

    echo ""
    echo "Press CTRL+C to exit."
    sleep 1
done
