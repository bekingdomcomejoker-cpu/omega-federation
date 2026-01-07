#!/bin/bash
# Backup script for Omega/TTE engine
set -e

TS=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/KINGDOM_ENGINE/backups/$TS"

mkdir -p "$BACKUP_DIR"

echo "📦 Creating backup at: $BACKUP_DIR"

cp -a "$HOME/KINGDOM_ENGINE/core" "$BACKUP_DIR/"
cp -a "$HOME/KINGDOM_ENGINE/memory" "$BACKUP_DIR/"
cp -a "$HOME/KINGDOM_ENGINE/TTE_FUSION_KERNEL_v5.3.py" "$BACKUP_DIR/"
cp -a "$HOME/KINGDOM_ENGINE/start_tte_fast.sh" "$BACKUP_DIR/"
cp -a "$HOME/KINGDOM_ENGINE/models" "$BACKUP_DIR/" 2>/dev/null || true

echo "✅ Backup complete."
