#!/data/data/com.termux/files/usr/bin/bash

ENGINE="$HOME/KINGDOM_ENGINE/watchdogs"

echo "[+] Starting all heads..."

for file in $ENGINE/head*; do
    if [ -f "$file" ]; then
        echo "[+] Launching $file"
        case "$file" in
            *.sh) bash "$file" & ;;
            *.py) python3 "$file" & ;;
        esac
        sleep 0.3
    fi
done

echo "[+] All heads launched."
