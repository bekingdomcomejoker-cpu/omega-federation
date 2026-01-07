#!/data/data/com.termux/files/usr/bin/bash
# HEAD 8 - realitynode
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head8_realitynode.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD8 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD8 | realitynode | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


MERKABAH="$ROOT/core/merkabah_core.py"

# Listen on named pipe
PIPE="$ROOT/reality_pipe"
[ -p "$PIPE" ] || mkfifo "$PIPE"

log "Reality Node listening on $PIPE"

while true; do
    if read -t 1 line < "$PIPE" 2>/dev/null; then
        [ -z "$line" ] && continue
        
        RESULT=$(echo "$line" | python3 "$MERKABAH" 2>/dev/null || echo "{}")
        FACE=$(echo "$RESULT" | jq -r ".merkabah.active_face // \"UNKNOWN\"" 2>/dev/null)
        
        log "VISION | Face: $FACE | Input: ${line:0:50}..."
        echo "$RESULT" >> "$ROOT/logs/reality_visions.log"
    fi
    
    sleep 0.1
done


log "CRASHED"
