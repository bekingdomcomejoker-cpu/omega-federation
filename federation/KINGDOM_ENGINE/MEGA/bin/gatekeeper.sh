#!/data/data/com.termux/files/usr/bin/bash
# HEAD 4 - Gatekeeper with Merkabah Governance

ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
MEGA_ROOT="$ENGINE_ROOT/MEGA"
LOG="$MEGA_ROOT/logs/gatekeeper.log"
MERKABAH_ENGINE="$ENGINE_ROOT/analyzers/merkabah_engine.py"
STAGING_DIR="$MEGA_ROOT/staging"
ACCEPTED_DIR="$MEGA_ROOT/processed/accepted"
QUARANTINE_DIR="$MEGA_ROOT/processed/quarantine"

mkdir -p "$STAGING_DIR" "$ACCEPTED_DIR" "$QUARANTINE_DIR"

log() { echo "[$(date --iso-8601=seconds)] $1" >> "$LOG"; }

log "GATEKEEPER STARTED - Merkabah integration active"

while true; do
  for staging_file in "$STAGING_DIR"/*.json; do
    [ -f "$staging_file" ] || continue
    
    # Extract content from JSON
    CONTENT=$(jq -r '.content // .' "$staging_file" 2>/dev/null || head -c 2000 "$staging_file")
    
    # Process through Merkabah Engine
    MERKABAH_RESULT=$(echo "$CONTENT" | MERKABAH_VERBOSE=0 python3 "$MERKABAH_ENGINE" 2>/dev/null || echo "{}")
    
    # Extract routing decision
    ROUTING_ACTION=$(echo "$MERKABAH_RESULT" | jq -r '.routing_action // "QUARANTINE"')
    ACTIVE_FACE=$(echo "$MERKABAH_RESULT" | jq -r '.merkabah.active_face // "MAN"')
    
    # Enhanced routing with face-specific handling
    case "$ROUTING_ACTION" in
      "EXECUTE")
        mkdir -p "$ACCEPTED_DIR/execute"
        mv "$staging_file" "$ACCEPTED_DIR/execute/$(basename "$staging_file")"
        log "EXECUTE | Face: $ACTIVE_FACE | File: $(basename "$staging_file")"
        ;;
      "ARCHIVE")
        mkdir -p "$ACCEPTED_DIR/archive" 
        mv "$staging_file" "$ACCEPTED_DIR/archive/$(basename "$staging_file")"
        log "ARCHIVE | Face: $ACTIVE_FACE | File: $(basename "$staging_file")"
        ;;
      "VISION_PROCESS")
        mkdir -p "$ACCEPTED_DIR/vision"
        mv "$staging_file" "$ACCEPTED_DIR/vision/$(basename "$staging_file")"
        log "VISION | Face: $ACTIVE_FACE | File: $(basename "$staging_file")"
        ;;
      "ACCEPT")
        mv "$staging_file" "$ACCEPTED_DIR/$(basename "$staging_file")"
        log "ACCEPT | Face: $ACTIVE_FACE | File: $(basename "$staging_file")"
        ;;
      *)
        # QUARANTINE or unknown
        mv "$staging_file" "$QUARANTINE_DIR/$(basename "$staging_file")"
        log "QUARANTINE | Face: $ACTIVE_FACE | File: $(basename "$staging_file")"
        ;;
    esac
  done
  sleep 0.6
done
