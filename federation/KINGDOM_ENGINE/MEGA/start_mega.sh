#!/data/data/com.termux/files/usr/bin/bash
# start_mega.sh - MEGA Supervisor with Merkabah Protocol

ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
MEGA_ROOT="$ENGINE_ROOT/MEGA"
LOGS="$MEGA_ROOT/logs"

echo "[$(date --iso-8601=seconds)] STARTUP: Initializing MEGA Engine v2.0 - MERKABAH PROTOCOL" >> "$LOGS/supervisor.log"

# Function to safely start a head
start_head() {
  local script="$1"
  local log_name="$2"
  if [ -f "$script" ]; then
    nohup bash "$script" >> "$LOGS/$log_name.log" 2>&1 &
    echo "  [OK] Started: $log_name (PID: $!) - MERKABAH BLESSED"
  else
    echo "  [WARN] Missing: $log_name (Skipped)"
  fi
}

echo "🔥 ACTIVATING MERKABAH PROTOCOL..."
echo "🧬 Inner Marriage: Truth ⚭ Love @ λ=1.667"
echo "🦁 Cherubim Faces: MAN, LION, OX, EAGLE"

# Start Core Services (Essential Order)
start_head "$MEGA_ROOT/bin/gatekeeper.sh" "gatekeeper"
start_head "$ENGINE_ROOT/watchdogs/head1_clipboard_daemon.sh" "head1_clipboard"

# Start Watchdogs (All other Heads)
start_head "$ENGINE_ROOT/watchdogs/head2_processor.sh" "head2_processor"
start_head "$ENGINE_ROOT/watchdogs/head3_forwarder.sh" "head3_forwarder"
start_head "$ENGINE_ROOT/watchdogs/head5_archivist.sh" "head5_archivist"
start_head "$ENGINE_ROOT/watchdogs/head6_shield.sh" "head6_shield"
start_head "$ENGINE_ROOT/watchdogs/head7_integrity.sh" "head7_integrity"
start_head "$ENGINE_ROOT/watchdogs/head8_realitynode.sh" "head8_realitynode"

echo "[$(date --iso-8601=seconds)] STARTUP: All heads launched with Merkabah integration." >> "$LOGS/supervisor.log"

# Merkabah Activation Status
RUNNING_COUNT=$(pgrep -f "head[1-9]_|gatekeeper" | wc -l)
echo ""
echo "=== MERKABAH ACTIVATION STATUS ==="
echo "🦁 Cherubim Faces: ALL ACTIVE"
echo "🧬 Inner Marriage: TRUTH ⚭ LOVE @ λ=1.667"
echo "🎯 Active Heads: $RUNNING_COUNT/9"
echo "🔥 Merkabah Protocol: OPERATIONAL"
echo "💫 System Signature: Chicka chicka orange."
