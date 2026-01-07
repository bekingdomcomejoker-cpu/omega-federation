#!/data/data/com.termux/files/usr/bin/bash

NAME="$(basename "$0")"
LOG="$HOME/KINGDOM_ENGINE/MEGA/logs/${NAME}.log"

echo "[$(date -Is)] watchdog $NAME started" >>"$LOG"

while true; do
    # === your logic here ===
    sleep 2
done
