#!/data/data/com.termux/files/usr/bin/bash

INBOX="$HOME/KINGDOM_ENGINE/MEGA/inbox/headX"
LOG="$HOME/KINGDOM_ENGINE/MEGA/logs/headX_inbox.log"

process() {
    mkdir -p "$INBOX"
    for msg in "$INBOX"/*; do
        [ -f "$msg" ] || continue
        payload=$(cat "$msg")
        echo "$(date -Iseconds) [headX] RECEIVED: $payload" >> "$LOG"
        rm -f "$msg"
    done
}

while true; do
    sleep 0.3
    process
done
