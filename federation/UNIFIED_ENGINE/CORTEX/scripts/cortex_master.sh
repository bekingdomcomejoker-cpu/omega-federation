#!/data/data/com.termux/files/usr/bin/bash

LOGDIR=~/UNIFIED_ENGINE/logs
OUT=~/UNIFIED_ENGINE/CORTEX/output/cortex_summary.txt
CACHE=~/UNIFIED_ENGINE/CORTEX/cache/state.hash

calc_hash() {
    find "$LOGDIR" -type f -exec sha256sum {} \; | sort | sha256sum
}

# Load previous hash
OLD=""
[ -f "$CACHE" ] && OLD=$(cat "$CACHE")

while true; do
    NEW=$(calc_hash)

    if [ "$NEW" != "$OLD" ]; then
        echo "=== $(date) ===" > "$OUT"
        for L in "$LOGDIR"/*.log; do
            echo "--- $(basename "$L") ---" >> "$OUT"
            tail -n 10 "$L" >> "$OUT"
            echo "" >> "$OUT"
        done
        
        echo "$NEW" > "$CACHE"
    fi

    sleep 60
done
