#!/data/data/com.termux/files/usr/bin/bash
INBOX="$HOME/KINGDOM_ENGINE/MEGA/inbox/head6"
LOG="$HOME/KINGDOM_ENGINE/MEGA/logs/head6_inbox.log"

mkdir -p "$INBOX"

process_inbox() {
    for msg in "$INBOX"/*; do
        [ -f "$msg" ] || continue
        payload=$(cat "$msg")
        echo "$(date -Iseconds) [head6] RECEIVED: $payload" >> "$LOG"
        rm -f "$msg"
    done
}

while true; do
    sleep 0.3
    process_inbox
done
