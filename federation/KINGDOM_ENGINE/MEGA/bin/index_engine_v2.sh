#!/data/data/com.termux/files/usr/bin/bash

OUT="$HOME/KINGDOM_ENGINE/MEGA/state/engine_index_v2.json"

echo '{ "generated": "'$(date -Is)'", "files": [' > "$OUT"

find "$HOME/KINGDOM_ENGINE" -type f | while read f; do
    size=$(stat -c%s "$f")
    mod=$(stat -c%y "$f")
    echo '  { "path": "'$f'", "size": '$size', "modified": "'$mod'" },' >> "$OUT"
done

echo '] }' >> "$OUT"

echo "[indexer] updated: $OUT"

