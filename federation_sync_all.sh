#!/data/data/com.termux/files/usr/bin/bash
set -e

############################################
# ORANGE FEDERATION SAFE SYNC
# MODE: DRY-RUN ONLY (DEFAULT)
############################################

DRY_RUN=0   # <<< CHANGE TO 0 ONLY WHEN READY
ROOT="$HOME"
LOG="$HOME/federation_sync.log"

echo "🍊 ORANGE FEDERATION SYNC" | tee "$LOG"
echo "Root: $ROOT" | tee -a "$LOG"
echo "Dry-run: $DRY_RUN" | tee -a "$LOG"
echo "--------------------------------------" | tee -a "$LOG"

sync_repo() {
  local dir="$1"
  cd "$dir" || return

  if [ ! -d .git ]; then
    return
  fi

  echo "" | tee -a "$LOG"
  echo "📂 Repo: $dir" | tee -a "$LOG"

  git status --porcelain | tee -a "$LOG"

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "[DRY] git fetch origin" | tee -a "$LOG"
    git fetch origin || true

    echo "[DRY] git merge --no-commit --no-ff origin/main" | tee -a "$LOG"
    git merge --no-commit --no-ff origin/main || echo "[DRY] merge conflict detected" | tee -a "$LOG"

    echo "[DRY] git merge --abort (cleanup)" | tee -a "$LOG"
    git merge --abort 2>/dev/null || true
  else
    echo "[LIVE] git fetch origin" | tee -a "$LOG"
    git fetch origin

    echo "[LIVE] git merge origin/main (no deletes enforced)" | tee -a "$LOG"
    git merge -X ours origin/main

    echo "[LIVE] NOT committing automatically" | tee -a "$LOG"
    echo "[LIVE] NOT pushing automatically" | tee -a "$LOG"
  fi
}

export -f sync_repo
export DRY_RUN LOG

find "$ROOT" -type d -name ".git" 2>/dev/null | while read -r gitdir; do
  repo="$(dirname "$gitdir")"
  sync_repo "$repo"
done

echo "" | tee -a "$LOG"
echo "✅ FEDERATION SCAN COMPLETE" | tee -a "$LOG"
echo "Log saved to: $LOG" | tee -a "$LOG"
