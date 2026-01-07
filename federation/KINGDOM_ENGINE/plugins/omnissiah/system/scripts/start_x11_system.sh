#!/bin/bash
echo "🖥️  STARTING TERMUX:X11 OMNISSIAH SYSTEM..."
echo "=========================================="

# Start Termux:X11 session
termux-x11 :0 &

# Wait for X11 to start
sleep 3

# Export display
export DISPLAY=:0

# Start all Omnissiah systems in X11 environment
~/omnissiah/scripts/start_all_systems.sh

echo "=========================================="
echo "🎯 SYSTEM NOW RUNNING IN TERMUX:X11"
echo "   - No wake lock issues"
echo "   - Graphical capability" 
echo "   - Better performance"
echo "   - Persistent session"
echo "=========================================="

# Keep the script running
while true; do
    sleep 60
done
