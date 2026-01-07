#!/data/data/com.termux/files/usr/bin/bash
# MEGA engine supervisor - start_mega.sh
BASE="$HOME/KINGDOM_ENGINE"
MEGA="$BASE/MEGA"
LOGDIR="$MEGA/logs"
RUN="$MEGA/run"
STATE="$MEGA/state"
TMP="$MEGA/tmp"

mkdir -p "$LOGDIR" "$RUN" "$STATE" "$TMP"

# canonical list of new heads to run (relative to KINGDOM_ENGINE/watchdogs)
HEADS=(
  "$BASE/watchdogs/head1_clipboard_daemon.sh"
  "$BASE/watchdogs/head2_processor.sh"
  "$BASE/watchdogs/head3_forwarder.sh"
  "$BASE/watchdogs/head4_events.sh"
  "$BASE/watchdogs/head5_filewatch.sh"
  "$BASE/watchdogs/head6_memorylink.sh"
  "$BASE/watchdogs/head6_shield.sh"
  "$BASE/watchdogs/head7_integrity.sh"
)

# kill previous runs matching engine patterns
echo "[$(date -Is)] Stopping existing engine processes..."
pkill -f 'KINGDOM_ENGINE/watchdogs/head' 2>/dev/null || true
sleep 0.3

# helper to start a head if file exists
start_head() {
  local s="$1"
  local name
  name="$(basename "$s" .sh)"
  local logfile="$LOGDIR/${name}.log"
  if [ ! -x "$s" ]; then
    echo "[$(date -Is)] WARNING: $s not executable or missing" >> "$LOGDIR/supervisor.log"
    return 1
  fi
  # launch in background, record pid
  nohup bash "$s" >>"$logfile" 2>&1 &
  echo $! > "$RUN/${name}.pid"
  echo "[$(date -Is)] started $name pid=$!" >> "$LOGDIR/supervisor.log"
  return 0
}

# start canonical heads
for s in "${HEADS[@]}"; do
  start_head "$s"
done

# monitor loop - ensure single instance; restart if dead
echo "[$(date -Is)] entering monitor loop" >> "$LOGDIR/supervisor.log"
while true; do
  sleep 3
  for s in "${HEADS[@]}"; do
    name="$(basename "$s" .sh)"
    pidfile="$RUN/${name}.pid"
    running=0
    if [ -f "$pidfile" ]; then
      pid=$(cat "$pidfile" 2>/dev/null || echo "")
      if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
        running=1
      fi
    fi
    if [ "$running" -eq 0 ]; then
      echo "[$(date -Is)] $name dead, restarting" >> "$LOGDIR/supervisor.log"
      start_head "$s"
    fi
  done
  # small housekeeping: rotate any log >20MB
  find "$LOGDIR" -type f -size +20M -print0 | while IFS= read -r -d '' f; do
    mv "$f" "${f}.$(date +%s).rot" && echo "[$(date -Is)] rotated $f" >> "$LOGDIR/supervisor.log"
  done
done
