#!/data/data/com.termux/files/usr/bin/bash
pkill -f 'head[1-7]_' 2>/dev/null || true
sleep 0.2
for s in ~/KINGDOM_ENGINE/watchdogs/head*.sh; do
  nohup bash "$s" >/dev/null 2>&1 &
done
echo "started heads"
