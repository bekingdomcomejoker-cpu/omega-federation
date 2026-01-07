#!/data/data/com.termux/files/usr/bin/bash

OUT="$HOME/KINGDOM_ENGINE/MEGA/state/index.json"

echo '{' > "$OUT"
echo '  "generated": "'$(date -Is)'",' >>"$OUT"
echo '  "files": [' >>"$OUT"

find "$HOME/KINGDOM_ENGINE" -type f | sed 's/"/\\"/g' | sed 's/^/    "/' | sed 's/$/",/' >>"$OUT"

echo '  ]' >>"$OUT"
echo '}' >>"$OUT"

echo "index updated: $OUT"
