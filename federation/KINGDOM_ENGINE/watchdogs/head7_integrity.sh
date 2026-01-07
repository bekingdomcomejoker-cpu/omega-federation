#!/data/data/com.termux/files/usr/bin/bash
# HEAD 7 - integrity
ROOT="$HOME/KINGDOM_ENGINE"
MEGA="$ROOT/MEGA"
LOG="$ROOT/logs/head7_integrity.log"
HEARTBEAT="$ROOT/logs/heartbeat.log"
PID=$$

log() {
    echo "[$(date --iso-8601=seconds)] HEAD7 | $1" >> "$LOG"
    echo "[$(date --iso-8601=seconds)] HEAD7 | integrity | $1" >> "$HEARTBEAT"
}

log "STARTED (PID: $PID)"

trap 'log "STOPPED"; exit 0' SIGTERM SIGINT


while true; do
    PROC_COUNT=$(ps aux | grep -E "head[0-9]_" | grep -v grep | wc -l)
    log "INTEGRITY CHECK: $PROC_COUNT heads active"
    
    # Check for stuck files
    STUCK_INBOX=$(find "$MEGA/inbox" -type f -mmin +10 2>/dev/null | wc -l)
    STUCK_PROC=$(find "$MEGA/processing" -type f -mmin +5 2>/dev/null | wc -l)
    
    [ "$STUCK_INBOX" -gt 0 ] && log "WARNING: $STUCK_INBOX stuck files in inbox"
    [ "$STUCK_PROC" -gt 0 ] && log "WARNING: $STUCK_PROC stuck files in processing"
    
    sleep 10
done


log "CRASHED"
