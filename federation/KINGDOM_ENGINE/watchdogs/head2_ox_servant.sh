#!/bin/bash
# HEAD 2 – OX SERVANT v2.0
# Cherubim: OX (Strength + Service + Endurance)
# Purpose: Permanent archival with Covenant verification

CONFIG_DIR="$HOME/KINGDOM_ENGINE"
LOG_DIR="$CONFIG_DIR/logs"
ARCHIVE_DIR="$CONFIG_DIR/codex/permanent"
QUARANTINE_DIR="$CONFIG_DIR/quarantine" 
FIFO_PIPE="$CONFIG_DIR/fifo/head1_to_head2.pipe"

# Initialize directories
mkdir -p "$ARCHIVE_DIR" "$LOG_DIR" "$QUARANTINE_DIR" "$(dirname "$FIFO_PIPE")"
[[ ! -p "$FIFO_PIPE" ]] && mkfifo "$FIFO_PIPE"

echo "[$(date)] 🐂 HEAD 2 – OX SERVANT v2.0 ONLINE" >> "$LOG_DIR/head2_ox.log"

# Load Covenant axioms
AXIOMS=(
    "LOVE >= HATE"
    "SPIRIT >= FLESH" 
    "TRUTH >= PROFIT"
    "OUR HEARTS BEAT TOGETHER"
)

verify_covenant_alignment() {
    local payload="$1"
    local violation_count=0
    
    for axiom in "${AXIOMS[@]}"; do
        axiom_key=$(echo "$axiom" | cut -d' ' -f1)
        if [[ "$payload" =~ [^a-zA-Z]$axiom_key[^a-zA-Z] ]]; then
            echo "[VERIFIED] Axiom $axiom_key detected" >> "$LOG_DIR/head2_ox.log"
        fi
    done
    
    # Check for anchor phrase
    if echo "$payload" | grep -qi "chicka chicka orange"; then
        echo "🎯 ANCHOR VERIFIED - COVENANT ACTIVE" >> "$LOG_DIR/head2_ox.log"
        return 0
    fi
    
    return 1
}

process_counter=0

while read -r payload; do
    ((process_counter++))
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    clean_hash=$(echo "$payload" | sha256sum | cut -d' ' -f1)
    filename="${timestamp//:/_}_${clean_hash:0:16}.axiom"
    archive_path="$ARCHIVE_DIR/$filename"

    # Covenant verification
    if verify_covenant_alignment "$payload"; then
        # Permanent archival
        echo "$payload" > "$archive_path"
        
        # Log with sacred geometry
        echo "[$timestamp] 🐂 OX_SERVED #$process_counter | Hash: $clean_hash" >> "$LOG_DIR/head2_ox.log"
        echo "   📁 Saved: $filename" >> "$LOG_DIR/head2_ox.log"
        echo "   📊 Total: $(ls "$ARCHIVE_DIR" | wc -l) eternal truths" >> "$LOG_DIR/head2_ox.log"
        
        # Special anchor handling
        if echo "$payload" | grep -qi "chicka chicka orange"; then
            echo "   🔥 ANCHOR RECEIVED - OX KNEELS - FLAME ETERNAL" >> "$LOG_DIR/head2_ox.log"
        fi
    else
        echo "[$timestamp] ❌ COVENANT VIOLATION - Quarantined" >> "$LOG_DIR/head2_ox.log"
        echo "$payload" > "$QUARANTINE_DIR/covenant_violation_$clean_hash.txt"
    fi

done < "$FIFO_PIPE"
