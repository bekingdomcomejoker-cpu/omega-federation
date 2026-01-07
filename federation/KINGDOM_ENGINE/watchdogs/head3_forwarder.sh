#!/data/data/com.termux/files/usr/bin/bash
# HEAD 3 - forwarder
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head3_forwarder.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD3 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD3 | forwarder | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


while true; do
    for file in "$MEGA/processing"/*.json; do
        [ -f "$file" ] || continue
        
        BASENAME=$(basename "$file")
        mv "$file" "$MEGA/staging/$BASENAME" 2>/dev/null && log "FORWARDED: $BASENAME"
    done
    
    sleep 0.5
done


log "CRASHED"
