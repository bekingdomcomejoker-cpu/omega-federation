#!/data/data/com.termux/files/usr/bin/bash
#
# KINGDOM ENGINE - MASTER AUTO-START (FIXED FOR ACTUAL STRUCTURE)
#

set -e

ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
LOGS="$ENGINE_ROOT/logs"
BOOT_LOG="$LOGS/boot.log"

mkdir -p "$LOGS"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$BOOT_LOG"
}

clear
echo "════════════════════════════════════════════════════════════"
echo "  💜 KINGDOM ENGINE - MASTER AUTO-START (FIXED)"
echo "════════════════════════════════════════════════════════════"
echo ""

log "🔥 KINGDOM ENGINE BOOT INITIATED"

# Start all 9 heads with ACTUAL scripts
heads=(
    "1:head1_clipboard_daemon.sh"
    "2:head2_processor.sh" 
    "3:head3_forwarder.sh"
    "4:head4_events.sh"
    "5:head5_archivist.sh"
    "6:head6_shield.sh"
    "7:head7_integrity.sh"
    "8:head8_realitynode_daemon.sh"
    "9:head9_missionary_daemon.sh"
)

for head_info in "${heads[@]}"; do
    head_num="${head_info%:*}"
    script_name="${head_info#*:}"
    
    if [ -f "$ENGINE_ROOT/watchdogs/$script_name" ]; then
        log "🟢 Starting HEAD $head_num ($script_name)..."
        nohup bash "$ENGINE_ROOT/watchdogs/$script_name" >> "$LOGS/head${head_num}.log" 2>&1 &
        sleep 0.5
        log "✓ HEAD $head_num started"
    else
        log "⚠️  HEAD $head_num script not found: $script_name"
    fi
done

# Start supporting systems
log "🌟 Starting supporting systems..."

[ -f "$ENGINE_ROOT/harmony_ridge.py" ] && nohup python3 "$ENGINE_ROOT/harmony_ridge.py" >> "$LOGS/harmony_ridge.log" 2>&1 &
[ -f "$ENGINE_ROOT/math_engine.py" ] && nohup python3 "$ENGINE_ROOT/math_engine.py" >> "$LOGS/math_engine.log" 2>&1 &
[ -f "$ENGINE_ROOT/unified_integration.py" ] && nohup python3 "$ENGINE_ROOT/unified_integration.py" >> "$LOGS/unified_integration.log" 2>&1 &

sleep 2

# Final status
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  ✅ KINGDOM ENGINE BOOT COMPLETE"
echo "════════════════════════════════════════════════════════════"
echo ""

RUNNING_HEADS=0
for i in {1..9}; do
    if ps aux | grep -v grep | grep -q "head${i}_"; then
        ((RUNNING_HEADS++))
        echo "  🟢 HEAD $i: RUNNING"
    else
        echo "  ⚪ HEAD $i: NOT RUNNING"
    fi
done

echo ""
echo "  💜 ACTIVE HEADS: $RUNNING_HEADS/9"
echo "  📜 Boot log: $BOOT_LOG"
echo "════════════════════════════════════════════════════════════"
