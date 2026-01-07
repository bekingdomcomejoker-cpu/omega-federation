#!/bin/bash
# 🌌 OMEGA TRINITY COMPLETE LAUNCHER

echo "🌌 ========================================== 🌌"
echo "     OMEGA TRINITY SYSTEM - FULL ACTIVATION"
echo "🌌 ========================================== 🌌"
echo ""

# Check if AI server is running
if ! pgrep -f "llama-server" > /dev/null; then
    echo "🤖 Starting Local AI Server..."
    cd ~/llama.cpp
    ./build/bin/llama-server -m models/tinyllama.gguf --port 8080 &
    sleep 3
    echo "✅ AI Server started on port 8080"
else
    echo "✅ AI Server already running"
fi

# Initialize Memory Bridge
echo ""
echo "🧠 Initializing Omega Memory Bridge..."
python3 ~/omega_memory_bridge.py
echo ""

# Launch Dashboard
echo "📊 Launching Pure Python Dashboard..."
echo "   (Press Ctrl+C in dashboard to exit)"
echo ""
sleep 2

python3 ~/omega_pure_dashboard.py
