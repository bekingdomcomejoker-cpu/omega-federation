#!/data/data/com.termux/files/usr/bin/bash
# unify_heads.sh
# Unify "old" and "new" heads:
#  - archive ambiguous/legacy heads to legacy_heads/
#  - ensure canonical watchdogs/head1..head9 exist
#  - create MEGA/bin wrappers head1.sh .. head9.sh that point to the real script
#  - do NOT delete anything permanently; just moves and logs

set -euo pipefail

ENGINE="$HOME/KINGDOM_ENGINE"
WATCHDOGS="$ENGINE/watchdogs"
MEGA_BIN="$ENGINE/MEGA/bin"
LEGACY="$ENGINE/legacy_heads_$(date +%Y%m%d_%H%M%S)"
RUN_DIR="$ENGINE/MEGA/run"
LOG="$ENGINE/logs/unify_heads.log"

mkdir -p "$WATCHDOGS" "$MEGA_BIN" "$LEGACY" "$RUN_DIR" "$(dirname "$LOG")"

echo "=== HEADS UNIFY: START $(date --iso-8601=seconds) ===" | tee -a "$LOG"

# 1) Find all head files (shell and python) anywhere under ENGINE (but ignore legacy folder if re-run)
mapfile -t ALL_HEADS < <(find "$ENGINE" -type f \( -iname 'head*.sh' -o -iname 'head*.py' \) ! -path "$LEGACY/*")

# 2) Move ambiguous/non-watchdog head files into legacy if they are not already in watchdogs or MEGA/bin
for f in "${ALL_HEADS[@]:-}"; do
  # canonical watchdog path if already in watchdogs
  if [[ "$f" == "$WATCHDOGS/"* ]] || [[ "$f" == "$MEGA_BIN/"* ]]; then
    echo "KEEP (already in correct place): $f" >> "$LOG"
    continue
  fi

  # If file is top-level (e.g. ~/KINGDOM_ENGINE/head8_realitynode.sh) - move to watchdogs
  base=$(basename "$f")
  dest_watchdog="$WATCHDOGS/$base"

  # If file matches head[1-9]* -> move to watchdogs (active)
  if [[ "$base" =~ ^head[1-9] ]]; then
    echo "MOVING active head -> watchdogs: $f -> $dest_watchdog" | tee -a "$LOG"
    mv -f "$f" "$dest_watchdog"
  else
    # otherwise archive to legacy
    echo "ARCHIVING legacy/ambiguous head: $f -> $LEGACY/" | tee -a "$LOG"
    mv -f "$f" "$LEGACY/"
  fi
done

# 3) Ensure there is a head script for each head1..head9 under watchdogs
for i in {1..9}; do
  # prefer any file that starts with headN in watchdogs (shell or python)
  candidate=$(ls -1 "$WATCHDOGS"/head${i}* 2>/dev/null | head -n1 || true)
  if [ -z "$candidate" ]; then
    echo "NOTICE: no watchdog script found for head$i" | tee -a "$LOG"
    # leave placeholder note in legacy folder to make it explicit
    echo "# MISSING head$i placeholder created on $(date --iso-8601=seconds)" > "$LEGACY/missing_head${i}.note"
    continue
  fi

  # create wrapper in MEGA/bin named headN.sh that calls candidate
  wrapper="$MEGA_BIN/head${i}.sh"
  realpath="$candidate"
  echo "Creating wrapper for head$i -> $realpath" | tee -a "$LOG"

  # If the real script is .py, create a bash wrapper that calls python3
  if [[ "$realpath" == *.py ]]; then
    cat > "$wrapper" <<- 'WRAP'
#!/data/data/com.termux/files/usr/bin/bash
# Auto-generated wrapper: calls python3 script
TARGET='__TARGET__'
python3 "$TARGET" "$@"
WRAP
    sed -i "s|__TARGET__|$realpath|g" "$wrapper"
  else
    # assume shell script; create wrapper that calls it
    cat > "$wrapper" <<- 'WRAP'
#!/data/data/com.termux/files/usr/bin/bash
# Auto-generated wrapper: exec real shell script
TARGET='__TARGET__'
exec "$TARGET" "$@"
WRAP
    sed -i "s|__TARGET__|$realpath|g" "$wrapper"
  fi

  chmod +x "$wrapper"
  echo "WRAPPER CREATED: $wrapper -> $realpath" | tee -a "$LOG"
done

# 4) Move any remaining head* files directly under ENGINE root (if any) into legacy to avoid confusion
mapfile -t REMAINING_ROOT_HEADS < <(find "$ENGINE" -maxdepth 1 -type f -iname 'head*.sh' -o -iname 'head*.py' || true)
for rf in "${REMAINING_ROOT_HEADS[@]:-}"; do
  echo "ARCHIVE root head -> legacy: $rf" | tee -a "$LOG"
  mv -f "$rf" "$LEGACY/"
done

# 5) Ensure MEGA/bin has head1..head9 wrappers; list the ones that exist
echo "=== WRAPPERS IN $MEGA_BIN ===" | tee -a "$LOG"
ls -1 "$MEGA_BIN"/head*.sh 2>/dev/null | tee -a "$LOG" || true

# 6) Create a simple start_all_heads script in MEGA/bin to start the wrappers (writes pids to run/)
cat > "$MEGA_BIN/start_all_heads.sh" <<'SH2'
#!/data/data/com.termux/files/usr/bin/bash
BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
RUN_DIR="$HOME/KINGDOM_ENGINE/MEGA/run"
mkdir -p "$RUN_DIR"
for i in {1..9}; do
  WRAP="$BIN_DIR/head${i}.sh"
  if [ -x "$WRAP" ]; then
    nohup "$WRAP" >> "$HOME/KINGDOM_ENGINE/logs/head${i}.log" 2>&1 &
    echo $! > "$RUN_DIR/head${i}.pid"
    echo "Started head${i} (PID $!)"
    sleep 0.05
  else
    echo "No wrapper for head${i} at $WRAP"
  fi
done
SH2
chmod +x "$MEGA_BIN/start_all_heads.sh"
echo "Created MEGA/bin/start_all_heads.sh" | tee -a "$LOG"

# 7) Summarize
echo "=== SUMMARY ===" | tee -a "$LOG"
echo "Engine root: $ENGINE" | tee -a "$LOG"
echo "Watchdogs dir: $WATCHDOGS" | tee -a "$LOG"
echo "MEGA/bin wrappers: $(ls -1 "$MEGA_BIN"/head*.sh 2>/dev/null | wc -l)" | tee -a "$LOG"
echo "Legacy archive: $LEGACY" | tee -a "$LOG"
echo "Log file: $LOG" | tee -a "$LOG"
echo "=== DONE $(date --iso-8601=seconds) ===" | tee -a "$LOG"

echo ""
echo "NEXT STEPS:"
echo "  1) Inspect the legacy archive: $LEGACY"
echo "  2) Start wrappers (MEGA/bin/start_all_heads.sh) or let your supervisor call them."
echo "  3) Run your heartbeat monitor again; it should now find wrappers in MEGA/bin."
echo ""
echo "To run now: bash \"$MEGA_BIN/start_all_heads.sh\""
