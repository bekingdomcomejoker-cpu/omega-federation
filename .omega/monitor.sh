#!/bin/bash
# OMEGA SYSTEM MONITOR

while true; do
    clear
    echo "⚔️ OMEGA SYSTEM MONITOR - λ = 3.340"
    echo "══════════════════════════════════════"
    echo "[$(date)]"
    echo ""
    
    # Network status
    echo "🌐 NETWORK STATUS:"
    ifconfig | grep -A1 "inet" | head -5
    echo ""
    
    # Process status
    echo "🔄 PROCESS STATUS:"
    ps aux | grep -E "(omega|ssh|python)" | grep -v grep
    echo ""
    
    # Connection status
    echo "📡 CONNECTIONS:"
    netstat -an | grep -E "(ESTABLISHED|LISTEN)" | head -5
    echo ""
    
    # Disk usage
    echo "💾 DISK USAGE:"
    df -h /data/data/com.termux/files
    echo ""
    
    echo "🍊 Chicka chicka orange"
    echo "🔥 Frequency locked at 3.340"
    
    sleep 5
done
