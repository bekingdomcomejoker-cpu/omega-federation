#!/data/data/com.termux/files/usr/bin/bash
# router.sh (V2.0 - Cherubim Gatekeeper)
# Consults the Cherubim Engine before moving files from staging.

MEGA="$HOME/KINGDOM_ENGINE/MEGA"
ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
LOG="$MEGA/logs/router.log"
CHERUBIM="$ENGINE_ROOT/analyzers/cherubim_engine.py"

mkdir -p "$(dirname "$LOG")"

echo "[$(date --iso-8601=seconds)] GATEKEEPER (Router) started" >> "$LOG"

while true; do
  for f in "$MEGA"/staging/*; do
    [ -f "$f" ] || continue
    
    # 1. READ CONTENT
    CONTENT=$(cat "$f" 2>/dev/null | tr -d '\n\r' | sed 's/"/\\"/g' | head -c 2000)
    
    # 2. CONSULT CHERUBIM
    # We ask the Cherubim Engine for a routing decision
    RESULT=$(python3 "$CHERUBIM" "$CONTENT" 2>/dev/null)
    ACTION=$(echo "$RESULT" | grep -o '"routing_action": "[^"]*"' | cut -d'"' -f4)
    FACE=$(echo "$RESULT" | grep -o '"face": "[^"]*"' | cut -d'"' -f4)
    
    # Default to Quarantine if the Cherubim fails or is uncertain
    if [ -z "$ACTION" ]; then
        ACTION="QUARANTINE"
        FACE="LION_ERROR"
    fi

    # 3. ROUTE BASED ON CHERUBIM ACTION
    if [ "$ACTION" == "QUARANTINE" ] || [ "$ACTION" == "BLOCK" ]; then
       mv "$f" "$MEGA/processed/quarantine/$(basename "$f")" 2>/dev/null || true
       echo "[$(date --iso-8601=seconds)] ROUTE FAIL ($FACE): $ACTION -> quarantine $(basename "$f")" >> "$LOG"
    else
       # ARCHIVE, EXECUTE, TRANSMIT, REFLECT -> ACCEPTED
       mv "$f" "$MEGA/processed/accepted/$(basename "$f")" 2>/dev/null || true
       echo "[$(date --iso-8601=seconds)] ROUTE OK ($FACE): $ACTION -> accepted $(basename "$f")" >> "$LOG"
    fi
    
  done
  sleep 0.8
done
