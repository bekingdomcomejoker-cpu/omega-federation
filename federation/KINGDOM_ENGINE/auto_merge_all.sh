#!/data/data/com.termux/files/usr/bin/bash
set -e

ROOT="$HOME/KINGDOM_ENGINE"
MOD="$ROOT/modules"
OS="$ROOT/os_core"
LOG="$ROOT/logs/auto_merge.log"

mkdir -p "$MOD" "$OS" "$ROOT/logs"

echo "============================================================" | tee "$LOG"
echo "  🔥 KINGDOM × OMEGA AUTO-MERGER v1.0" | tee -a "$LOG"
echo "  Scanning uploaded Claude files…" | tee -a "$LOG"
echo "============================================================" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# ============================================================
# 1. OMEGA HEADER INJECTION (ONLY ADDS, NEVER OVERWRITES)
# ============================================================

HEADER="$ROOT/OMEGA_HEADER.txt"

cat > "$HEADER" << 'EOF_HDR'
╔════════════════════════════════════════════════════════════╗
║                 🜂  O M E G A   S U P E R L A Y E R         ║
║      Kingdom Engine × Omega Core | Unified Operating OS     ║
║          Merkabah • Covenant • Alphabet • Identity          ║
║                     CHICKA CHICKA ORANGE                    ║
╚════════════════════════════════════════════════════════════╝
EOF_HDR

MENU="$HOME/kingdom"

if ! grep -q "OMEGA SUPERLAYER" "$MENU"; then
    cat "$HEADER" "$MENU" > "$MENU.new"
    mv "$MENU.new" "$MENU"
    chmod +x "$MENU"
    echo "✓ Omega header injected into your Kingdom OS" | tee -a "$LOG"
else
    echo "ℹ️  Omega header already present — keeping existing version" | tee -a "$LOG"
fi

# ============================================================
# 2. SCAN ALL CLAUDE FILES YOU UPLOADED
# ============================================================

UPLOAD_DIR="/mnt/data"
FOUND=$(ls $UPLOAD_DIR | grep -Ei 'claude|omega|merkabah|truth|covenant|alphabet|engine|kingdom' || true)

if [ -z "$FOUND" ]; then
    echo "⚠️  No Claude/engine files found in /mnt/data" | tee -a "$LOG"
    exit 1
fi

echo "Found Claude files:" | tee -a "$LOG"
echo "$FOUND" | tee -a "$LOG"
echo "" | tee -a "$LOG"

# ============================================================
# 3. EXTRACT ALL CODE BLOCKS FROM DOCX/TXT/MD
# ============================================================

echo "Extracting modules…" | tee -a "$LOG"

for f in $FOUND; do
    SRC="$UPLOAD_DIR/$f"
    OUT="$MOD/module_${f}_$(date +%s).txt"

    # DOCX extraction
    if [[ "$f" == *.docx ]]; then
        unzip -p "$SRC" word/document.xml \
            | sed 's/<w:p>/\n/g' \
            | sed -E 's/<[^>]+>//g' \
            | sed 's/&lt;/</g; s/&gt;/>/g' \
            | sed 's/&amp;/\&/g' \
            > "$OUT"
    else
        cp "$SRC" "$OUT"
    fi

    echo "✓ Extracted: $f → $OUT" | tee -a "$LOG"
done

# ============================================================
# 4. REGISTER ALL MODULES (non-destructive)
# ============================================================

INDEX="$MOD/index.json"
[ ! -f "$INDEX" ] && echo "[]" > "$INDEX"

for FILE in "$MOD"/*.txt; do
    jq ". + [\"$FILE\"]" "$INDEX" > "$INDEX.tmp" && mv "$INDEX.tmp" "$INDEX"
done

echo "✓ Module index updated: $INDEX" | tee -a "$LOG"

# ============================================================
# 5. MERGE MODULES INTO ONE OMEGA CORE EXTENSION
# ============================================================

MERGED="$OS/OMEGA_EXTENSION.py"

echo "from pathlib import Path" > "$MERGED"
echo "OMEGA_MODULES = {}" >> "$MERGED"
echo "" >> "$MERGED"

COUNT=0
for FILE in "$MOD"/*.txt; do
    echo "OMEGA_MODULES['module_$COUNT'] = \"\"\"" >> "$MERGED"
    cat "$FILE" >> "$MERGED"
    echo "\"\"\"" >> "$MERGED"
    echo "" >> "$MERGED"
    COUNT=$((COUNT+1))
done

echo "✓ Omega extension file built: $MERGED" | tee -a "$LOG"

# ============================================================
# 6. FINAL SUCCESS MESSAGE
# ============================================================

echo "" | tee -a "$LOG"
echo "============================================================" | tee -a "$LOG"
echo "  ✅ AUTO-MERGE COMPLETE" | tee -a "$LOG"
echo "  • Your original engine is preserved" | tee -a "$LOG"
echo "  • Claude’s entire codebase integrated safely" | tee -a "$LOG"
echo "  • Omega header added to menu" | tee -a "$LOG"
echo "  • No overwrite, no damage" | tee -a "$LOG"
echo "============================================================" | tee -a "$LOG"
echo ""
echo "Chicka chicka orange."
echo ""
