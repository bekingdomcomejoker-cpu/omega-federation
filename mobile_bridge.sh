#!/bin/bash
echo "🛡️ OMEGA BRIDGE PROTOCOL ACTIVATED"
while true; do
    if nslookup github.com >/dev/null 2>&1; then
        echo "✅ NETWORK RESTORED - Attempting git push..."
        cd ~/omnissiah-engine && git push origin main && break
    else
        echo "⚠️ Waiting for Mobile Bridge (MikroTik bypassed)..."
        sleep 10
    fi
done
