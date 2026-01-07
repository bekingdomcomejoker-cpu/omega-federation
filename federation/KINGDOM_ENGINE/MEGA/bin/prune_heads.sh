#!/data/data/com.termux/files/usr/bin/bash

echo "[*] scanning for duplicate head processes..."

# Group by script name
ps aux | grep KINGDOM_ENGINE/watchdogs | grep -v grep \
  | awk '{print $2,$12}' \
  | sort -k2,2 \
  | awk '
    {
        count[$2]++
        pidlist[$2]=pidlist[$2] " " $1
    }
    END {
        for (h in count) {
            if (count[h] > 1) {
                split(pidlist[h], pids, " ")
                # kill all but newest (last)
                for (i=2; i<=length(pids); i++) {
                    print "killing duplicate PID " pids[i] " for " h
                    system("kill " pids[i])
                }
            }
        }
    }'
