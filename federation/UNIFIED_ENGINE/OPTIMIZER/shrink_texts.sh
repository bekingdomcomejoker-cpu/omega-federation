#!/data/data/com.termux/files/usr/bin/bash

ROOT=~/UNIFIED_ENGINE

find "$ROOT" -type f -iname "*.txt" | while read -r f; do
    sed -i '
        /^\s*$/d
        s/[[:space:]]\+$//
    ' "$f"
done

echo "Shrink complete."
