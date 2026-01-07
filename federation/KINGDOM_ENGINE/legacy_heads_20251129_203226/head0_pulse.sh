#!/data/data/com.termux/files/usr/bin/bash
# head0_pulse.sh — HEARTBEAT VISUALIZER
# Reads logs and displays the real-time system pulse.

LOG_CHER=~/KINGDOM_ENGINE/logs/cherubim.log
LOG_HEAD1=~/KINGDOM_ENGINE/logs/head1_clipboard.log
LOG_GATE=~/KINGDOM_ENGINE/MEGA/logs/gatekeeper.log

pulse() {
    clear
    echo "=================================================="
    echo "            🔥 MEGA ENGINE HEARTBEAT 🔥"
    echo "=================================================="

    # Show last Cherubim decision
    C_LINE=$(tail -n 1 "$LOG_CHER")
    FACE=$(echo "$C_LINE" | grep -o '"face": *"[^"]*"' | sed 's/.*: "//;s/"$//')
    ACTION=$(echo "$C_LINE" | grep -o '"routing_action": *"[^"]*"' | sed 's/.*: "//;s/"$//')
    VECTOR=$(echo "$C_LINE" | grep -o '"vector": *"[^"]*"' | sed 's/.*: "//;s/"$//')

    # Render face bars
    case "$FACE" in
        LION)   BAR="███████";;
        OX)     BAR="█████";;
        EAGLE)  BAR="████";;
        MAN)    BAR="████████";;
        *)      BAR="██";;
    esac

    echo "FACE: $FACE   |   VECTOR: $VECTOR"
    echo "ACTION: $ACTION"
    echo "INTENSITY: $BAR"
    echo ""

    # Show last AXIOM scan
    A_LINE=$(tail -n 1 "$LOG_HEAD1")
    if echo "$A_LINE" | grep -q "AXIOM_VIOLATION"; then
        echo "AXIOMS: ❌ VIOLATION DETECTED"
    else
        echo "AXIOMS: ✔ CLEAN"
    fi
    echo ""

    # Show latest Gatekeeper route
    G_LINE=$(tail -n 1 "$LOG_GATE")
    echo "GATE: $G_LINE"
    echo ""

    echo "=================================================="
    echo "Updated: $(date '+%H:%M:%S')"
    echo "Press CTRL+C to exit."
}

while true; do
    pulse
    sleep 1
done
