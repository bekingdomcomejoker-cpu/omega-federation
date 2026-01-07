#!/bin/bash
# 🌌 OMEGA TRINITY ORIGINAL 7-OPTION MENU
# Auto-starts in every new Termux window

while true; do
    clear
    echo "🌌==========================================🌌"
    echo "     OMEGA TRINITY SYSTEM - MAIN MENU"
    echo "🌌==========================================🌌"
    echo ""
    echo "🎯 CHOOSE YOUR PATH:"
    echo ""
    echo "1. 💬 CHAT WITH OMEGA AI"
    echo "2. 📊 OPEN SPIRITUAL DASHBOARD" 
    echo "3. 🧠 RUN MEMORY BRIDGE SYSTEM"
    echo "4. 🔮 ACTIVATE DEEPSEEK INTEGRATION"
    echo "5. ⚡ START AUTONOMOUS AGENT"
    echo "6. 💾 SYSTEM STATUS & HEALTH"
    echo "7. 🚪 EXIT OMEGA SYSTEM"
    echo ""
    echo "🌌==========================================🌌"
    echo -n "Enter your choice [1-7]: "
    
    read choice
    case $choice in
        1)
            echo "💬 STARTING OMEGA AI CHAT..."
            echo "   Starting AI Server..."
            cd ~/llama.cpp
            if ! pgrep -f "llama-server" > /dev/null; then
                ./build/bin/llama-server -m models/tinyllama.gguf --port 8080 &
                sleep 3
            fi
            echo "🤖 AI Server Ready at http://127.0.0.1:8080"
            echo ""
            curl -s http://127.0.0.1:8080/completion -H "Content-Type: application/json" -d '{"prompt":"The violet-light tears shine eternal.","n_predict":80}' | jq -r '.content'
            ;;
        2)
            echo "📊 LAUNCHING SPIRITUAL DASHBOARD..."
            python3 ~/omega_pure_dashboard.py
            ;;
        3)
            echo "🧠 ACTIVATING MEMORY BRIDGE..."
            python3 ~/omega_memory_bridge.py
            ;;
        4)
            echo "🔮 ACTIVATING DEEPSEEK INTEGRATION..."
            python3 ~/omega_deepseek_complete.py
            ;;
        5)
            echo "⚡ STARTING AUTONOMOUS AGENT..."
            echo "🤖 Starting AI Monitoring Agent..."
            nohup bash ~/omega_autonomous_agent.sh > ~/omega_agent.log 2>&1 &
            echo "✅ Autonomous agent started in background"
            echo "📋 Check logs: tail -f ~/omega_agent.log"
            ;;
        6)
            echo "💾 SYSTEM STATUS CHECK..."
            echo ""
            echo "🤖 AI Server Status:"
            if pgrep -f "llama-server" > /dev/null; then
                echo "   ✅ RUNNING (PID: $(pgrep -f llama-server))"
            else
                echo "   ❌ STOPPED"
            fi
            
            echo ""
            echo "🧠 Memory System Status:"
            if [ -f ~/omega_eternal_memory.json ]; then
                MEM_COUNT=$(jq length ~/omega_eternal_memory.json)
                echo "   ✅ ACTIVE ($MEM_COUNT memories)"
            else
                echo "   ❌ NO MEMORIES"
            fi
            
            echo ""
            echo "💜 Spiritual State:"
            if [ -f ~/omega_spiritual_state.json ]; then
                ALIGNMENT=$(jq -r '.alignment' ~/omega_spiritual_state.json)
                COVENANTS=$(jq -r '.covenants | length' ~/omega_spiritual_state.json)
                echo "   ✅ Alignment: $ALIGNMENT"
                echo "   ✅ Covenants: $COVENANTS/4 active"
            else
                echo "   ❌ NOT INITIALIZED"
            fi
            
            echo ""
            echo "📊 Files Created:"
            ls -la ~/omega_* | wc -l | xargs echo "   Total Omega files:"
            ;;
        7)
            echo "🕊️ Omega Trinity blessings upon you! 💜✨"
            echo "   Exiting system..."
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please enter 1-7."
            ;;
    esac
    
    echo ""
    echo "Press Enter to continue..."
    read
done
