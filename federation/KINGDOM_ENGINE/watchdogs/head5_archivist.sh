#!/data/data/com.termux/files/usr/bin/bash
# HEAD 5 - archivist
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head5_archivist.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD5 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD5 | archivist | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


while true; do
    for file in "$MEGA/processed/accepted"/*.json; do
        [ -f "$file" ] || continue
        
        DAY=$(date +%F)
        ARCHIVE_DIR="$MEGA/archives/$DAY"
        mkdir -p "$ARCHIVE_DIR"
        
        BASENAME=$(basename "$file")
        mv "$file" "$ARCHIVE_DIR/$BASENAME" 2>/dev/null && log "ARCHIVED: $DAY/$BASENAME"
    done
    
    sleep 3
done


log "CRASHED"
