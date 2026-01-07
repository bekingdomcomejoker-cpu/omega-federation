#!/bin/bash
# Restore script
set -e

DIR="$1"

if [ -z "$DIR" ]; then
  echo "Usage: restore_engine.sh <backup-folder>"
  exit 1
fi

echo "♻ Restoring from: $DIR"

cp -a "$DIR/core" "$HOME/KINGDOM_ENGINE/"
cp -a "$DIR/memory" "$HOME/KINGDOM_ENGINE/"
cp -a "$DIR/TTE_FUSION_KERNEL_v5.3.py" "$HOME/KINGDOM_ENGINE/"
cp -a "$DIR/start_tte_fast.sh" "$HOME/KINGDOM_ENGINE/"
cp -a "$DIR/models" "$HOME/KINGDOM_ENGINE/" 2>/dev/null || true

echo "🔥 Restore complete."
