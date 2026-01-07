#!/data/data/com.termux/files/usr/bin/bash
MEGA="$HOME/KINGDOM_ENGINE/MEGA"
LOG="$MEGA/logs/event_bus.log"
mkdir -p "$(dirname "$LOG")"

echo "[$(date --iso-8601=seconds)] event_bus started" >> "$LOG"

# Lightweight event bus: watches inbox and notifies router by creating "route" markers
while true; do
  # any new json in inbox/*/* ?
  for d in "$MEGA"/inbox/*; do
    [ -d "$d" ] || continue
    for f in "$d"/*.json; do
      [ -f "$f" ] || continue
      # create a route request
      cp "$f" "$MEGA/staging/$(basename "$d")_$(basename "$f")" 2>/dev/null || true
      echo "[$(date --iso-8601=seconds)] event_bus routed $(basename "$f")" >> "$LOG"
      rm -f "$f"
    done
  done
  sleep 0.6
done
