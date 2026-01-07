#!/data/data/com.termux/files/usr/bin/bash
#
# HEAD 9 – GOD NODE (OUTBOUND)
# Temperance / Self-Control
# Safe outward expression of processed truth
#

set -e

ENGINE_ROOT=~/KINGDOM_ENGINE
OUTBOX=$ENGINE_ROOT/outbox
LOG=$ENGINE_ROOT/logs/head9_outbound.log
PID=$ENGINE_ROOT/pids/head9.pid

mkdir -p "$OUTBOX" "$(dirname "$LOG")" "$(dirname "$PID")"

echo $$ > "$PID"

log() {
    echo "[$(date '+%Y-%m-%dT%H:%M:%S')] $1" | tee -a "$LOG"
}

log "=== HEAD 9 – GOD NODE / OUTBOUND STARTED ==="
log "Outbox: $OUTBOX"

# MAIN LOOP
while true; do
    for file in "$OUTBOX"/*.txt; do
        [ -e "$file" ] || continue
        
        basename=$(basename "$file")
        log "OUTBOUND DETECTED: $basename"

        content=$(cat "$file")

        # Controlled, safe, non-automatic expression
        echo "$content" | termux-clipboard-set
        log "CLIPBOARD UPDATED FROM OUTBOUND: $basename"

        mv "$file" "$OUTBOX/sent_$basename"
        log "ARCHIVED: sent_$basename"
    done
    
    sleep 1
done
