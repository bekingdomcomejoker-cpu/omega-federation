#!/data/data/com.termux/files/usr/bin/bash

OUT="$HOME/KINGDOM_ENGINE/MEGA/dashboard/engine_status.json"

echo '{' > "$OUT"
echo '"time":"'"$(date -Is)"'",' >> "$OUT"
echo '"heads":[' >> "$OUT"

ps aux | grep watchdogs | grep -v grep | awk '{print "  \""$12"\","}' >> "$OUT"

echo '],' >> "$OUT"
echo '"disk":' >> "$OUT"
df -h $HOME | sed 's/"/\\"/g' | awk 'NR>1 {print "  \""$0"\""}' >> "$OUT"

echo '}' >> "$OUT"
