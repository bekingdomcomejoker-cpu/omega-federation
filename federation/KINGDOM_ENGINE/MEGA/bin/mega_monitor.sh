# AUTO-WAKE CHECK
if ! pgrep -f wakelock.sh >/dev/null; then
  echo "💤 Wakelock inactive — reactivating..."
  bash ~/KINGDOM_ENGINE/MEGA/bin/wakelock.sh &
else
  echo "⚡ Wakelock active — Termux prevented from sleeping."
fi
