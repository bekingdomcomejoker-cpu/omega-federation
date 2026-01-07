#!/data/data/com.termux/files/usr/bin/bash

for H in ~/UNIFIED_ENGINE/watchdogs/head*.sh; do
    nohup bash "$H" >/dev/null 2>&1 &
done

echo "All 7 Watchdogs launched."
