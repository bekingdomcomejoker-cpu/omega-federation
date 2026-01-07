#!/usr/bin/env bash
# Head 5 - Archivist

set -euo pipefail
LOGDIR="$HOME/KINGDOM_ENGINE/logs"
ARCH="$HOME/KINGDOM_ENGINE/backups"
IDX="$HOME/KINGDOM_ENGINE/indices/document_index.txt"

mkdir -p "$LOGDIR" "$ARCH" "$(dirname "$IDX")"

TS=$(date +"%Y%m%d_%H%M%S")
OUT="$ARCH/docs_$TS.tar.gz"
DOCS="$HOME/storage/shared"

EX="pdf txt md doc docx xls xlsx ppt pptx odt ods csv epub"

> "$IDX"
for e in $EX; do
  find "$DOCS" -type f -iname "*.$e" >> "$IDX" 2>/dev/null || true
done

sort -o "$IDX" "$IDX"
tar -czf "$OUT" -T "$IDX" 2>/dev/null || true
echo "$(date +"%FT%T") archived $OUT" >> "$LOGDIR/archivist.log"
