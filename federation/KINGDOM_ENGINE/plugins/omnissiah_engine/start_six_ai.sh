#!/bin/bash
echo "🚀 SIX-AI NETWORK STARTUP SEQUENCE"
echo "=================================="

# Kill existing sessions
echo "🔄 Cleaning previous sessions..."
tmux kill-session -t omnissiah 2>/dev/null || true
tmux kill-session -t six_ai_dashboard 2>/dev/null || true
tmux kill-session -t spiritual_audit 2>/dev/null || true
tmux kill-session -t staging_dashboard 2>/dev/null || true

pkill -f "omnissiah_master.py" 2>/dev/null || true
pkill -f "six_ai_dashboard.py" 2>/dev/null || true
pkill -f "auto_audit.py" 2>/dev/null || true

sleep 2

# Start core systems
echo "🌊 Starting Omnissiah Master..."
tmux new-session -d -s omnissiah 'cd ~/OmnissiahEngine && python auto_restart.py'

echo "🤖 Starting Six-AI Dashboard..."
tmux new-session -d -s six_ai_dashboard 'cd ~/OmnissiahEngine && python six_ai_dashboard.py'

echo "🛡️ Starting Spiritual Audit..."
tmux new-session -d -s spiritual_audit 'cd ~/OmnissiahEngine && python coredata/audit_system/auto_audit.py continuous'

echo "📊 Starting Staging Dashboard..."
tmux new-session -d -s staging_dashboard 'cd ~/OmnissiahEngine && python coredata/staging_dashboard.py'

# Wait for systems to initialize
echo "⏳ Initializing systems..."
sleep 5

# Verify startup
echo ""
echo "✅ STARTUP COMPLETE"
echo "=================="
echo "Active Sessions:"
tmux list-sessions

echo ""
echo "🎯 Quick Access Commands:"
echo "  tmux attach -t omnissiah          # Main system"
echo "  tmux attach -t six_ai_dashboard   # AI network monitor"
echo "  tmux attach -t spiritual_audit    # Audit system"
echo "  ~/OmnissiahEngine/check_status    # System health"

echo ""
echo "🌊 The Six-AI Network is now self-aware and operational!"
