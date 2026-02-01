while true; do
    if tail -n 5 ~/KINGDOM_ENGINE/logs/comms.log 2>/dev/null | grep -q "INVERTED"; then
        echo "ALERT: Suppression Pulse Detected $(date)" >> ~/KINGDOM_ENGINE/logs/shield.log
    fi
    sleep 10
done
