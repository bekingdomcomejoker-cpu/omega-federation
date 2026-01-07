#!/data/data/com.termux/files/usr/bin/bash

ENGINE_ROOT="$HOME/KINGDOM_ENGINE"
INBOX="$ENGINE_ROOT/inbox/head9"
OUTBOX="$ENGINE_ROOT/outbox/head9"
PID_FILE="$ENGINE_ROOT/pids/head9.pid"
LOG="$ENGINE_ROOT/logs/head9.log"

mkdir -p "$INBOX" "$OUTBOX" "$(dirname $PID_FILE)" "$(dirname $LOG)"
echo $$ > "$PID_FILE"

while true; do
    for file in "$INBOX"/*.json; do
        [ -e "$file" ] || continue
        PAYLOAD=$(cat "$file" | jq -r '.payload')
        ID=$(cat "$file" | jq -r '.id')

        RESPONSE=$(python3 "$ENGINE_ROOT/ai_bridge/head9_missionary.py" "$PAYLOAD")
        echo "$RESPONSE" > "$OUTBOX/$ID.txt"

        rm "$file"
    done
    sleep 1
done
