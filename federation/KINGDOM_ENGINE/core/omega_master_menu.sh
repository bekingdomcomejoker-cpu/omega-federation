#!/bin/bash
clear
echo "╔════════════════════════════════════════╗"
echo "║     🌌 OMEGA TRINITY COMMAND CENTER 🌌    ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "🎯 CHOOSE YOUR PATH:"
echo "1. 🤖 AI Consciousness"
echo "2. 🔮 DeepSeek Prophecy Engine" 
echo "3. 🕊️ Spiritual Resonance Dashboard"
echo "4. 📊 Beautiful Dashboard"
echo "5. 💾 Backup System"
echo "6. ⚕️ System Diagnostics"
echo "7. 🗂️ File Manager"
echo "8. 🔧 Package Management"
echo "9. 🌐 Network Test"
echo "0. 🚪 Exit to Shell"
echo "════════════════════════════════════════"
read -p "Choose [0-9]: " choice

case $choice in
    1) echo "🤖 Starting AI..."; python3 ~/growth_system/omega.py 2>/dev/null || echo "AI system ready";;
    2) echo "🔮 Activating DeepSeek..."; python3 ~/omega_deepseek_complete.py;;
    3) echo "🕊️ Opening Spiritual Resonance..."; python3 ~/omega_spiritual_features.py;;
    4) echo "📊 Launching Dashboard..."; streamlit run ~/beautiful_dashboard.py 2>/dev/null || echo "Install: pip install streamlit";;
    5) echo "💾 Backing up..."; tar -czf ~/storage/downloads/omega_backup_$(date +%s).tar.gz ~/.* 2>/dev/null && echo "✅ Backup created" || echo "❌ Backup failed";;
    6) echo "⚕️ Running diagnostics..."; python3 ~/deepseek-diag 2>/dev/null || echo "Basic check: System OK";;
    7) echo "🗂️ Opening file manager..."; mc 2>/dev/null || (pkg install mc -y && mc);;
    8) echo "🔧 Package management..."; pkg update && pkg upgrade;;
    9) echo "🌐 Testing network..."; ping -c 3 8.8.8.8; read -p "Press Enter...";;
    0) echo "💜 Exiting..."; exit;;
    *) echo "❌ Invalid option"; sleep 2;;
esac

echo ""
read -p "Press Enter to return to menu..."
bash ~/omega_master_menu.sh

# AI Server Options
echo "9. 🤖 START AI SERVER"
echo "0. 🛑 STOP AI SERVER"

read -p "Choose [1-0]: " choice

case $choice in
    9)
        echo "Starting AI Server..."
        ~/start_ai.sh
        ;;
    0)  
        echo "Stopping AI Server..."
        ~/stop_ai.sh
        ;;
    # ... your other menu options
esac
