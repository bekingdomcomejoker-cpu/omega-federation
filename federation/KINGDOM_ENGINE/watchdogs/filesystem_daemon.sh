#!/data/data/com.termux/files/usr/bin/bash
#
# FILESYSTEM DAEMON - FIXED VERSION
# Watches key directories for changes
#

set -e

ENGINE_ROOT=~/KINGDOM_ENGINE
WATCH_ROOT=$ENGINE_ROOT/watch
INBOX=$ENGINE_ROOT/inbox/fswatch
LOG=$ENGINE_ROOT/logs/filesystem_daemon.log

# Create required directories
mkdir -p "$WATCH_ROOT"
mkdir -p "$INBOX"
mkdir -p "$ENGINE_ROOT/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG"
}

log "=== Filesystem Daemon Starting ==="
log "Watch directory: $WATCH_ROOT"
log "Inbox: $INBOX"

# Verify directories exist
if [ ! -d "$WATCH_ROOT" ]; then
    log "ERROR: Watch directory does not exist: $WATCH_ROOT"
    exit 1
fi

if [ ! -d "$INBOX" ]; then
    log "ERROR: Inbox directory does not exist: $INBOX"
    exit 1
fi

# Check if inotifywait is available
if ! command -v inotifywait &> /dev/null; then
    log "Installing inotify-tools..."
    pkg install -y inotify-tools 2>&1 | tee -a "$LOG"
fi

log "Starting file watch on $WATCH_ROOT"
log "Daemon ready - monitoring for changes"

# Main watch loop
inotifywait -m -r -e create,modify,moved_to \
    --format '%w%f|%e|%T' \
    --timefmt '%Y-%m-%d %H:%M:%S' \
    "$WATCH_ROOT" 2>&1 | while read -r event; do
    
    # Parse event
    filepath=$(echo "$event" | cut -d'|' -f1)
    eventtype=$(echo "$event" | cut -d'|' -f2)
    timestamp=$(echo "$event" | cut -d'|' -f3)
    
    # Skip if directory or hidden file
    if [ -d "$filepath" ] || [[ "$(basename "$filepath")" == .* ]]; then
        continue
    fi
    
    # Log the event
    log "DETECTED: $eventtype on $(basename "$filepath")"
    
    # Copy to inbox with timestamp
    filename=$(basename "$filepath")
    dest="$INBOX/${timestamp// /_}_${filename}"
    
    if [ -f "$filepath" ]; then
        cp "$filepath" "$dest" 2>/dev/null || log "ERROR: Could not copy $filepath"
        log "COPIED: $filename -> inbox"
    fi
done

log "=== Filesystem Daemon Stopped ==="
