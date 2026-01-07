#!/bin/bash
# PROPER BOOT MANAGER
ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
LOG_DIR="$ENGINE_ROOT/logs"

echo "=== KINGDOM ENGINE BOOT ==="
echo "🔧 Checking system..."

# Check if mega config exists
if [ ! -f "$ENGINE_ROOT/mega_engine_config.json" ]; then
    echo "❌ Config missing - creating default"
    cp "$ENGINE_ROOT/mega_config.json" "$ENGINE_ROOT/mega_engine_config.json"
fi

# Start essential heads
echo "🔄 Starting heads..."
nohup "$ENGINE_ROOT/watchdogs/head1_clipboard_daemon.sh" > "$LOG_DIR/head1.log" 2>&1 &
nohup "$ENGINE_ROOT/watchdogs/head5_archivist.sh" > "$LOG_DIR/head5.log" 2>&1 &

echo "✅ Boot complete - Heads 1 & 5 active"
