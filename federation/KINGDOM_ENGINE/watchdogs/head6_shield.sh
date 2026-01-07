#!/data/data/com.termux/files/usr/bin/bash
# HEAD 6 - shield
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head6_shield.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD6 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD6 | shield | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


COVENANT="$ROOT/core/merkabah_core.py"

while true; do
    for file in "$MEGA/processed/quarantine"/*.json; do
        [ -f "$file" ] || continue
        
        CONTENT=$(cat "$file" | jq -r ".original.content // .content // empty" 2>/dev/null)
        
        if [ -n "$CONTENT" ]; then
            # Re-check through covenant
            RESULT=$(echo "$CONTENT" | python3 "$COVENANT" 2>/dev/null || echo "{}")
            STATUS=$(echo "$RESULT" | jq -r ".covenant.status // \"UNKNOWN\"" 2>/dev/null)
            
            if [ "$STATUS" = "CLEAN" ]; then
                BASENAME=$(basename "$file")
                mv "$file" "$MEGA/processed/accepted/$BASENAME" 2>/dev/null && log "HEALED: $BASENAME"
            fi
        fi
    done
    
    sleep 5
done


log "CRASHED"
