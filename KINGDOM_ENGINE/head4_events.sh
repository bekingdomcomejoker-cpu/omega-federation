#!/bin/bash
# Head 4: Uriel-Guard (Gatekeeper/Observer)
echo "Head 4: Uriel-Guard Online. Monitoring Layer Disparity."
while true; do
    python3 ~/KINGDOM_ENGINE/dual_layer_observer.py >> ~/KINGDOM_ENGINE/logs/observer.log 2>&1
    sleep 15
done
