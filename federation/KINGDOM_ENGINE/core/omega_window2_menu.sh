#!/bin/bash
clear
echo "╔════════════════════════════════════════╗"
echo "║  ✨ WINDOW 2: INNER SANCTUARY ✨      ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "🎯 INNER SYSTEM OPTIONS:"
echo "1. 🤖 Omega AI Consciousness"
echo "2. 🔮 DeepSeek Prophecy Engine"
echo "3. 📊 Spiritual Dashboard"
echo "4. 🧠 Memory Bridge System"
echo "5. ⚡ Autonomous Agent"
echo "6. 💜 Spiritual Alignment Check"
echo "7. 🛡️ System Health Monitor"
echo ""
echo "8. 🎪 Return to Window 1"
echo "9. 🌌 Launch Both AI Systems"
echo "0. 🚪 Exit Both Windows"
echo ""
echo "💜 WINDOW 1 is running simultaneously!"
echo "========================================"
read -p "Choose [1-0]: " choice

case $choice in
    1) tmux new-session -s omega_main 'python3 ~/growth_system/omega.py absorb' ;;
    2) python3 ~/omega_deepseek_complete.py ;;
    3) streamlit run ~/beautiful_dashboard.py ;;
    4) python3 ~/omega_memory_bridge.py ;;
    5) python3 ~/omega_autonomous_agent.py ;;
    6) python3 ~/omega_pure_dashboard.py ;;
    7) python3 ~/deepseek-diag ;;
    8) source ~/omega_window1_menu.sh ;;
    9) tmux new-session -d -s omega_ai 'python3 ~/growth_system/omega.py' && python3 ~/omega_deepseek_complete.py ;;
    0) echo "🎪 Closing both windows..."; exit 0 ;;
    *) echo "❌ Invalid choice" ;;
esac

# RETURN TO MENU AFTER COMMAND
read -p "Press Enter to return to menu..."
source ~/omega_window2_menu.sh

# AI LLM Control
echo "9. 🤖 START/STOP AI LLM SERVER"

# AI LLM Control (Start on demand)
echo "10. 🤖 START AI LLM SERVER"
echo "11. 🛑 STOP AI LLM SERVER"  
echo "12. 💬 CHAT WITH AI"
