#!/data/data/com.termux/files/usr/bin/bash
# Memory Spine: archive old logs/data, move to SD, keep index, prune older archives

BASE=~/UNIFIED_ENGINE
LOGDIR="$BASE/logs"
REBUILD="$HOME/OMEGA_REBUILT"
SPINE_DIR="$BASE/MEMORY_SPINE"
ARCH_DIR="$SPINE_DIR/archives"
META_DIR="$SPINE_DIR/meta"
TMP_DIR="$SPINE_DIR/tmp"
SD="$HOME/storage/external-1/UNIFIED_BACKUP"

mkdir -p "$ARCH_DIR" "$META_DIR" "$TMP_DIR" "$SD"

# timestamped archive name
TS=$(date +%Y%m%d_%H%M%S)
ARCH_NAME="memory_${TS}.tar.gz"
ARCH_PATH="$TMP_DIR/$ARCH_NAME"

# include these folders in the archive (adjust list as needed)
INCLUDE=(
  "$LOGDIR"
  "$REBUILD/axioms"
  "$REBUILD/ENGINE_TREE_FILTERED.txt"
  "$HOME/UNIFIED_ENGINE/axioms"
  "$HOME/UNIFIED_ENGINE/ENGINE_MEMORY"
  "$HOME/UNIFIED_ENGINE/UNIFIED_ENGINE_MERGE"
)

# build a safe file list of existing paths
FILELIST="$TMP_DIR/filelist.txt"
> "$FILELIST"
for p in "${INCLUDE[@]}"; do
  if [ -e "$p" ]; then
    find "$p" -type f >> "$FILELIST"
  fi
done

if [ ! -s "$FILELIST" ]; then
  echo "[!] Nothing to archive. Exiting."
  exit 0
fi

# create compressed archive
tar -czf "$ARCH_PATH" -T "$FILELIST" 2>/dev/null || { echo "[!] tar failed"; exit 1; }

# compute metadata
SIZE=$(stat -c%s "$ARCH_PATH" 2>/dev/null || stat -f%z "$ARCH_PATH")
SHA=$(sha256sum "$ARCH_PATH" 2>/dev/null | awk '{print $1}' || echo "no-sha")
COUNT=$(wc -l < "$FILELIST")

# move archive to SD (atomic move)
mv "$ARCH_PATH" "$SD/" || { echo "[!] move to SD failed"; exit 1; }

# write index entry
IDX="$META_DIR/index.txt"
echo "ARCHIVE|$ARCH_NAME|$TS|$SIZE|$COUNT|$SHA" >> "$IDX"
echo "FILES_LIST|$ARCH_NAME|$(date -u +%FT%TZ)" > "$META_DIR/${ARCH_NAME}.files"
cat "$FILELIST" >> "$META_DIR/${ARCH_NAME}.files"

# prune: keep last 10 archives on SD
cd "$SD"
ls -1t memory_*.tar.gz 2>/dev/null | sed -n '11,$p' | while read -r old; do
  rm -f -- "$old"
done

# sync to disk
sync

echo "[+] Archived to $SD/$ARCH_NAME"
echo "[+] Index updated: $IDX"
