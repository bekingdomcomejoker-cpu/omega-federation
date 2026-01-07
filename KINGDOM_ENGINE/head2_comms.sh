while true; do
    for f in ~/KINGDOM_ENGINE/inbox/*; do
        if [ -f "$f" ]; then
            echo "[$(date)] Transmitting $(basename "$f")" >> ~/KINGDOM_ENGINE/logs/comms.log
            python3 ~/KINGDOM_ENGINE/harmony_ridge.py < "$f" >> ~/KINGDOM_ENGINE/logs/comms.log
        fi
    done
    sleep 5
done
