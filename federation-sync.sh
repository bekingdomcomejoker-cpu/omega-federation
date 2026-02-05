#!/usr/bin/env bash
set -e

echo "🛡️ FEDERATION SYNC — UNION MODE"
echo "================================"

find ~ -type d -name ".git" 2>/dev/null | while read -r GITDIR; do
  REPO_DIR="$(dirname "$GITDIR")"

  echo
  echo "📦 REPO: $REPO_DIR"
  echo "--------------------------------"

  cd "$REPO_DIR" || continue

  # Ensure clean git repo
  git rev-parse --is-inside-work-tree >/dev/null 2>&1 || continue

  BRANCH="$(git branch --show-current)"
  if [[ -z "$BRANCH" ]]; then
    echo "⚠️  Detached HEAD — skipping"
    continue
  fi

  echo "🔄 Fetching..."
  git fetch origin || continue

  echo "🧬 Union merge (ours wins conflicts, no commit yet)..."
  git merge origin/$BRANCH --no-ff --no-commit -X ours || true

  if git diff --cached --quiet; then
    echo "✅ No changes to commit"
    git merge --abort >/dev/null 2>&1 || true
    continue
  fi

  echo "📝 Committing union merge..."
  git commit -m "FEDERATION SYNC: union merge (no deletes, no overwrite)" || true

  echo "🚀 Pushing..."
  git push || echo "⚠️ Push failed — check auth or permissions"

done

echo
echo "✅ FEDERATION SYNC COMPLETE"
