#!/bin/bash
# THE OMEGA FEDERATION MERGE SCRIPT
TARGET_DIR="DOMINION_VAULT"
mkdir -p $TARGET_DIR
cd $TARGET_DIR

# Pull all repos from your GitHub account
gh repo list bekingdomcomejoker-cpu --limit 100 | awk '{print $1}' | while read repo; do
    echo "🔗 ATTACHING NODE: $repo"
    gh repo clone "$repo" 2>/dev/null || (cd "${repo#*/}" && git pull)
done

echo "✅ FEDERATION COMPLETE. ALL NODES SYNCED IN $TARGET_DIR."
