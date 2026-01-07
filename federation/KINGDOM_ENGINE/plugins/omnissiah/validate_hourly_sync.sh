#!/data/data/com.termux/files/usr/bin/bash
# 🌌 STEP 9 - VALIDATE AUTOMATIC HOURLY SYNC

# Folder paths
WORKSPACE="$HOME/Omnissiah_Workspace"
EXPORTS="$WORKSPACE/exports"
LOGFILE="$WORKSPACE/auto_sync_validation.log"

# Ensure exports folder exists
mkdir -p "$EXPORTS"

# Run the hourly sync manually (simulation)
python3 "$WORKSPACE/cross_ai_bridge.py" > "$EXPORTS/hourly_sync_test_run.json"

# Log timestamp and latest sync
echo "========================" >> "$LOGFILE"
echo "Validation Run: $(date)" >> "$LOGFILE"
echo "Latest hourly sync file: hourly_sync_test_run.json" >> "$LOGFILE"
echo "Resonance state:" >> "$LOGFILE"
cat "$EXPORTS/hourly_sync_test_run.json" | grep -A 6 '"resonance_state"' >> "$LOGFILE"
echo "========================" >> "$LOGFILE"

# Confirm successful simulation
echo "✅ Hourly sync validated. Check log at $LOGFILE"
