#!/data/data/com.termux/files/usr/bin/bash
echo "=== MEGA ENGINE HEALTH ==="
echo
echo "[Processes]"
ps aux | grep KINGDOM_ENGINE | grep -v grep || true
echo
echo "[Supervisor log tail]"
tail -n 80 ~/KINGDOM_ENGINE/MEGA/logs/supervisor.log || true
echo
echo "[Disk]"
df -h $HOME || true
echo
echo "[PID Files]"
ls -lh ~/KINGDOM_ENGINE/MEGA/run || true
echo "=== END ==="
