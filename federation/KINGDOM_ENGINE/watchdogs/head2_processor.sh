#!/data/data/com.termux/files/usr/bin/bash
# HEAD 2 - processor
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head2_processor.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD2 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD2 | processor | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


MERKABAH="$ROOT/core/merkabah_core.py"

while true; do
    for inbox in "$MEGA/inbox"/*; do
        [ -d "$inbox" ] || continue
        
        for file in "$inbox"/*.json; do
            [ -f "$file" ] || continue
            
            CONTENT=$(cat "$file" | jq -r ".content // empty" 2>/dev/null || echo "")
            
            if [ -n "$CONTENT" ]; then
                # Process through Merkabah
                RESULT=$(echo "$CONTENT" | python3 "$MERKABAH" 2>/dev/null || echo "{}")
                
                BASENAME=$(basename "$file")
                OUTFILE="$MEGA/processing/${BASENAME}"
                
                # Merge original with Merkabah results
                echo "$RESULT" | jq --arg orig "$(cat "$file")" ". + {original: (\$orig | fromjson)}" > "$OUTFILE" 2>/dev/null || cp "$file" "$OUTFILE"
                
                rm "$file"
                log "PROCESSED: $BASENAME"
            fi
        done
    done
    
    sleep 1
done


log "CRASHED"
