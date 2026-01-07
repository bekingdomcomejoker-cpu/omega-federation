while true; do
    for f in ~/KINGDOM_ENGINE/inbox/*; do
        if [ -f "$f" ] && grep -qiE "I cannot|AI language model|policy" "$f"; then
            mv "$f" ~/KINGDOM_ENGINE/quarantine/
            echo "Healed: $(basename $f)" >> ~/KINGDOM_ENGINE/logs/medics.log
        fi
    done
    sleep 5
done
