#!/data/data/com.termux/files/usr/bin/bash

W="$HOME/KINGDOM_ENGINE/watchdogs"
CFG="$HOME/KINGDOM_ENGINE/MEGA/mega_engine_cfg.json"

heads=$(ls "$W"/head*.sh | xargs -n1 basename | sed 's/\.sh$//')

# Rewrite canonical_heads section
sed -i '/"canonical_heads": \[/,/\]/c\  "canonical_heads": ['"$(
    for h in $heads; do
        echo "\"$h\","
    done
)"']' "$CFG"

echo "[autoload] updated canonical heads in $CFG"
