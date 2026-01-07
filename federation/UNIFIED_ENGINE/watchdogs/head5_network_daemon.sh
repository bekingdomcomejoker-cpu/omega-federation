#!/data/data/com.termux/files/usr/bin/bash
LOG=~/UNIFIED_ENGINE/logs/head5_network.log
LAST=""

while true; do
    NEW=$(ip addr show | grep "inet " | sha256sum)
    if [ "$NEW" != "$LAST" ]; then
        echo "$(date) | NETWORK STATE CHANGED" >> "$LOG"
        LAST="$NEW"
    fi
    sleep 4
done
