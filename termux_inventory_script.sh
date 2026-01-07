#!/data/data/com.termux/files/usr/bin/bash

# ============================================
# KINGDOM_ENGINE: Termux Environment Inventory
# ============================================
# Run this script in Termux to analyze your current setup
# Usage: bash termux_inventory_script.sh

echo "=========================================="
echo "OMEGA FEDERATION: Environment Inventory"
echo "=========================================="
echo ""

# Create output directory
REPORT_DIR="$HOME/federation_inventory_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$REPORT_DIR"

echo "📁 Report will be saved to: $REPORT_DIR"
echo ""

# ==================== SECTION 1: DIRECTORY SIZE ====================
echo "1️⃣  Analyzing directory sizes..."
echo "-------------------------------------------"

if [ -d "$HOME/federation" ]; then
    echo "Federation directory found: $HOME/federation"
    du -sh "$HOME/federation" 2>/dev/null
    du -sh "$HOME/federation"/* 2>/dev/null | sort -h > "$REPORT_DIR/01_directory_sizes.txt"
    echo "✓ Saved to: 01_directory_sizes.txt"
else
    echo "⚠️  No ~/federation directory found. Checking current directory..."
    du -sh . 2>/dev/null
    du -sh ./* 2>/dev/null | sort -h > "$REPORT_DIR/01_directory_sizes.txt"
fi
echo ""

# ==================== SECTION 2: MODEL FILES ====================
echo "2️⃣  Locating AI model files (.gguf)..."
echo "-------------------------------------------"

if [ -d "$HOME/federation" ]; then
    find "$HOME/federation" -type f -name "*.gguf" -exec du -sh {} \; 2>/dev/null | sort -h > "$REPORT_DIR/02_model_files.txt"
else
    find . -type f -name "*.gguf" -exec du -sh {} \; 2>/dev/null | sort -h > "$REPORT_DIR/02_model_files.txt"
fi

MODEL_COUNT=$(wc -l < "$REPORT_DIR/02_model_files.txt")
echo "Found $MODEL_COUNT model files"
if [ "$MODEL_COUNT" -gt 0 ]; then
    cat "$REPORT_DIR/02_model_files.txt"
fi
echo "✓ Saved to: 02_model_files.txt"
echo ""

# ==================== SECTION 3: SCRIPTS ====================
echo "3️⃣  Cataloging shell scripts..."
echo "-------------------------------------------"

if [ -d "$HOME/federation" ]; then
    find "$HOME/federation" -type f -name "*.sh" -exec ls -lh {} \; 2>/dev/null > "$REPORT_DIR/03_shell_scripts.txt"
else
    find . -type f -name "*.sh" -exec ls -lh {} \; 2>/dev/null > "$REPORT_DIR/03_shell_scripts.txt"
fi

SCRIPT_COUNT=$(wc -l < "$REPORT_DIR/03_shell_scripts.txt")
echo "Found $SCRIPT_COUNT shell scripts"
echo "✓ Saved to: 03_shell_scripts.txt"
echo ""

# ==================== SECTION 4: PYTHON FILES ====================
echo "4️⃣  Cataloging Python files..."
echo "-------------------------------------------"

if [ -d "$HOME/federation" ]; then
    find "$HOME/federation" -type f -name "*.py" -exec ls -lh {} \; 2>/dev/null > "$REPORT_DIR/04_python_files.txt"
else
    find . -type f -name "*.py" -exec ls -lh {} \; 2>/dev/null > "$REPORT_DIR/04_python_files.txt"
fi

PYTHON_COUNT=$(wc -l < "$REPORT_DIR/04_python_files.txt")
echo "Found $PYTHON_COUNT Python files"
echo "✓ Saved to: 04_python_files.txt"
echo ""

# ==================== SECTION 5: LARGE FILES ====================
echo "5️⃣  Identifying large files (>10MB)..."
echo "-------------------------------------------"

if [ -d "$HOME/federation" ]; then
    find "$HOME/federation" -type f -size +10M -exec ls -lh {} \; 2>/dev/null | sort -k5 -h > "$REPORT_DIR/05_large_files.txt"
else
    find . -type f -size +10M -exec ls -lh {} \; 2>/dev/null | sort -k5 -h > "$REPORT_DIR/05_large_files.txt"
fi

LARGE_COUNT=$(wc -l < "$REPORT_DIR/05_large_files.txt")
echo "Found $LARGE_COUNT files larger than 10MB"
if [ "$LARGE_COUNT" -gt 0 ]; then
    head -10 "$REPORT_DIR/05_large_files.txt"
fi
echo "✓ Saved to: 05_large_files.txt"
echo ""

# ==================== SECTION 6: LOG FILES ====================
echo "6️⃣  Locating log files..."
echo "-------------------------------------------"

if [ -d "$HOME/federation" ]; then
    find "$HOME/federation" -type f -name "*.log" -exec du -sh {} \; 2>/dev/null | sort -h > "$REPORT_DIR/06_log_files.txt"
else
    find . -type f -name "*.log" -exec du -sh {} \; 2>/dev/null | sort -h > "$REPORT_DIR/06_log_files.txt"
fi

LOG_COUNT=$(wc -l < "$REPORT_DIR/06_log_files.txt")
echo "Found $LOG_COUNT log files"
echo "✓ Saved to: 06_log_files.txt"
echo ""

# ==================== SECTION 7: DOCUMENTATION ====================
echo "7️⃣  Cataloging documentation files..."
echo "-------------------------------------------"

if [ -d "$HOME/federation" ]; then
    find "$HOME/federation" -type f \( -name "*.md" -o -name "*.txt" -o -name "*.doc" -o -name "*.docx" \) -exec ls -lh {} \; 2>/dev/null > "$REPORT_DIR/07_documentation.txt"
else
    find . -type f \( -name "*.md" -o -name "*.txt" -o -name "*.doc" -o -name "*.docx" \) -exec ls -lh {} \; 2>/dev/null > "$REPORT_DIR/07_documentation.txt"
fi

DOC_COUNT=$(wc -l < "$REPORT_DIR/07_documentation.txt")
echo "Found $DOC_COUNT documentation files"
echo "✓ Saved to: 07_documentation.txt"
echo ""

# ==================== SECTION 8: DIRECTORY TREE ====================
echo "8️⃣  Creating directory tree..."
echo "-------------------------------------------"

if [ -d "$HOME/federation" ]; then
    find "$HOME/federation" -type d 2>/dev/null | head -50 > "$REPORT_DIR/08_directory_tree.txt"
else
    find . -type d 2>/dev/null | head -50 > "$REPORT_DIR/08_directory_tree.txt"
fi

echo "✓ Saved to: 08_directory_tree.txt"
echo ""

# ==================== SECTION 9: LLAMA.CPP ====================
echo "9️⃣  Checking for llama.cpp..."
echo "-------------------------------------------"

if [ -d "$HOME/federation/llama.cpp" ]; then
    echo "✓ llama.cpp found"
    du -sh "$HOME/federation/llama.cpp" > "$REPORT_DIR/09_llama_cpp_info.txt"
    ls -lh "$HOME/federation/llama.cpp" | head -20 >> "$REPORT_DIR/09_llama_cpp_info.txt"
    cat "$REPORT_DIR/09_llama_cpp_info.txt"
else
    echo "⚠️  llama.cpp not found in ~/federation/"
    echo "Not found" > "$REPORT_DIR/09_llama_cpp_info.txt"
fi
echo ""

# ==================== SECTION 10: SUMMARY ====================
echo "🔟  Generating summary..."
echo "-------------------------------------------"

cat > "$REPORT_DIR/00_SUMMARY.txt" <<EOF
OMEGA FEDERATION ENVIRONMENT INVENTORY
Generated: $(date)

DIRECTORY SIZES:
$(cat "$REPORT_DIR/01_directory_sizes.txt" 2>/dev/null | head -10)

MODEL FILES: $MODEL_COUNT files
SHELL SCRIPTS: $SCRIPT_COUNT files
PYTHON FILES: $PYTHON_COUNT files
LARGE FILES (>10MB): $LARGE_COUNT files
LOG FILES: $LOG_COUNT files
DOCUMENTATION: $DOC_COUNT files

TOTAL ENVIRONMENT SIZE:
$(du -sh "$HOME/federation" 2>/dev/null || du -sh . 2>/dev/null)

RECOMMENDATIONS:
1. Model files (.gguf) should NOT be uploaded to GitHub
2. Large log files should be cleaned or archived
3. llama.cpp directory should be excluded (use build scripts instead)
4. Only scripts, configs, and docs should go to GitHub

NEXT STEPS:
- Review the individual report files in: $REPORT_DIR
- Share this report with your AI assistant for organization strategy
- Run the organization scripts to prepare for GitHub upload
EOF

cat "$REPORT_DIR/00_SUMMARY.txt"
echo ""

# ==================== COMPLETION ====================
echo "=========================================="
echo "✅ INVENTORY COMPLETE"
echo "=========================================="
echo ""
echo "📊 Full report saved to:"
echo "   $REPORT_DIR"
echo ""
echo "📋 Files generated:"
ls -1 "$REPORT_DIR"
echo ""
echo "🚀 Next step: Share the 00_SUMMARY.txt with your AI assistant"
echo "   to get customized organization commands."
echo ""
echo "To view summary:"
echo "   cat $REPORT_DIR/00_SUMMARY.txt"
echo ""
