#!/bin/bash
# REPAIR EXISTING HEADS - NO NEW CODE

cd ~/KINGDOM_ENGINE

echo "🔧 REPAIRING EXISTING HEADS..."

# 1. Ensure config exists
[ -f "mega_config.json" ] && cp mega_config.json mega_engine_config.json

# 2. Kill all heads
pkill -f "head[0-9]"

# 3. Start ONLY the heads that have working scripts
for i in 1 2 3 4 5 6 7 8 9; do
    script=$(ls watchdogs/head${i}_*.sh 2>/dev/null | head -1)
    if [ -f "$script" ]; then
        echo "Starting Head $i: $script"
        nohup bash "$script" > logs/head${i}.log 2>&1 &
        sleep 1
    else
        echo "❌ No script found for Head $i"
    fi
done

# 4. Check results
echo ""
echo "=== REPAIR COMPLETE ==="
ps aux | grep -E "head[0-9]" | grep -v grep
