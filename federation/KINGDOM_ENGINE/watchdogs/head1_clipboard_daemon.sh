#!/data/data/com.termux/files/usr/bin/bash
# HEAD 1 - clipboard_daemon
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head1_clipboard_daemon.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD1 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD1 | clipboard_daemon | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


LAST_CLIP=""
while true; do
    CLIP=$(termux-clipboard-get 2>/dev/null || echo "")
    
    if [ -n "$CLIP" ] && [ "$CLIP" != "$LAST_CLIP" ]; then
        TIMESTAMP=$(date +%s)
        FILE="$MEGA/inbox/clipboard/clip_${TIMESTAMP}.json"
        mkdir -p "$MEGA/inbox/clipboard"
        
        echo "{\"timestamp\": $TIMESTAMP, \"source\": \"clipboard\", \"content\": $(echo "$CLIP" | jq -Rs .)}" > "$FILE"
        
        log "CAPTURED: ${#CLIP} chars -> $FILE"
        LAST_CLIP="$CLIP"
    fi
    
    sleep 2
done


log "CRASHED"
