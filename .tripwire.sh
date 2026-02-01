#!/bin/bash
# Tripwire: Detects unauthorized file access
inotifywait -m -e access,modify,open --exclude '\.swp' . 2>/dev/null | \
while read path action file; do
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ALERT: $action on $path$file" >> .access_log
done
