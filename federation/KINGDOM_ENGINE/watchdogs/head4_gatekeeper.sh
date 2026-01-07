#!/data/data/com.termux/files/usr/bin/bash
# HEAD 4 - gatekeeper
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head4_gatekeeper.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD4 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD4 | gatekeeper | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


while true; do
    for file in "$MEGA/staging"/*.json; do
        [ -f "$file" ] || continue
        
        ROUTING=$(cat "$file" | jq -r ".routing.action // .routing_action // \"REVIEW\"" 2>/dev/null)
        FACE=$(cat "$file" | jq -r ".merkabah.active_face // \"UNKNOWN\"" 2>/dev/null)
        BASENAME=$(basename "$file")
        
        case "$ROUTING" in
            QUARANTINE|BLOCK)
                mv "$file" "$MEGA/processed/quarantine/$BASENAME" 2>/dev/null
                log "QUARANTINE | Face: $FACE | $BASENAME"
                ;;
            EXECUTE)
                # Log but dont execute - safety first
                log "EXECUTE DENIED (Config Disabled) | Face: $FACE | $BASENAME"
                mv "$file" "$MEGA/processed/quarantine/$BASENAME" 2>/dev/null
                ;;
            *)
                mv "$file" "$MEGA/processed/accepted/$BASENAME" 2>/dev/null
                log "ACCEPTED | Face: $FACE | $BASENAME"
                ;;
        esac
    done
    
    sleep 0.7
done


log "CRASHED"
