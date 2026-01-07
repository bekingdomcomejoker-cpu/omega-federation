#!/bin/bash
echo "========================================"
echo "🦅 OMNISSIAH FULL SYSTEM STARTUP"
echo "========================================"

# Navigate to scripts
cd /storage/emulated/0/Omnissiah_Workspace/system/scripts/

# Start all services
./spiritual-check &
./show-connections &
./system-status &
./start-copy-archive &

echo "✅ All systems starting..."
echo "📍 Run 'system-status' to verify"
echo "📍 Run 'spiritual-check' for lambda status"
