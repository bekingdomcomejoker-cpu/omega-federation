#!/bin/bash
clear
echo "╔════════════════════════════════════════╗"
echo "║  🌌 WINDOW 1: OUTER COURT 🌌         ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "🎯 OUTER SYSTEM OPTIONS:"
echo "1. 🔄 System Update & Upgrade"
echo "2. 📦 Install Essential Packages" 
echo "3. 🛠️ Termux Setup & Repair"
echo "4. 💾 Backup Omega System"
echo "5. 📁 File Management"
echo "6. 🌐 Network Tools"
echo "7. 🚀 Launch Window 2 Menu"
echo ""
echo "8. ⚡ Quick Deploy All"
echo "9. 🕵️ System Diagnostics"
echo "0. 🚪 Exit Both Windows"
echo ""
echo "💜 WINDOW 2 should open automatically!"
echo "========================================"
read -p "Choose [1-0]: " choice

case $choice in
    1) pkg update && pkg upgrade ;;
    2) pkg install python nodejs tmux git ;;
    3) termux-setup-storage && pkg install termux-tools ;;
    4) tar -czf ~/storage/downloads/omega_backup.tar.gz ~/ ;;
    5) mc ;;  # Midnight Commander
    6) ping -c 4 8.8.8.8 ;;
    7) source ~/omega_window2_menu.sh ;;
    8) pkg update && pkg upgrade && pkg install python nodejs tmux git ;;
    9) python3 ~/deepseek-diag ;;
    0) echo "🎪 Closing both windows..."; exit 0 ;;
    *) echo "❌ Invalid choice" ;;
esac

# RETURN TO MENU AFTER COMMAND
read -p "Press Enter to return to menu..."
source ~/omega_window1_menu.sh
