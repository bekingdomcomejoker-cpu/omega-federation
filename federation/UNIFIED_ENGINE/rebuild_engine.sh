#!/usr/bin/env bash
set -euo pipefail
DRYRUN=false
SRC="${HOME}/storage/shared/AI-TTE"
OUT="${HOME}/UNIFIED_ENGINE"
TMP="$OUT/_tmp"

for arg in "$@"; do
  case "$arg" in
    --dryrun) DRYRUN=true ;;
    --src=*) SRC="${arg#--src=}" ;;
    --out=*) OUT="${arg#--out=}" ;;
  esac
done

mkdir -p "$OUT" "$TMP"
mkdir -p "$OUT/ENGINE_CORE/knowledge_bank" \
         "$OUT/ENGINE_CORE/axioms" \
         "$OUT/ENGINE_CORE/chronicle" \
         "$OUT/ENGINE_CORE/trees" \
         "$OUT/ENGINE_MEMORY/chat_memory" \
         "$OUT/ENGINE_MEMORY/extracted_docs" \
         "$OUT/ENGINE_KERNEL/modules" \
         "$OUT/SCRIPTS" \
         "$OUT/LOGS"

echo "=== PHASE 1: COPY TEXT FILES ==="
find "$SRC" -type f \( -iname '*.md' -o -iname '*.txt' -o -iname '*.json' -o -iname '*.py' -o -iname '*.sh' -o -iname '*.docx' -o -iname '*.pdf' \) -print0 \
 | xargs -0 -I{} cp -n "{}" "$OUT" 2>>"$OUT/LOGS/rebuild.log" || true

echo "=== PHASE 2: DEDUPE ==="
find "$OUT" -type f -print0 | xargs -0 sha256sum > "$TMP/checksums.txt"
awk '{ if (!seen[$1]++) print; else print > "duplicate_records.txt" }' "$TMP/checksums.txt"

echo "=== PHASE 3: CONVERT DOCX/PDF ==="
find "$OUT" -type f \( -iname '*.docx' -o -iname '*.pdf' \) -size -10M -print0 \
 | while IFS= read -r -d '' f; do
     pandoc "$f" -t plain -o "$OUT/ENGINE_MEMORY/extracted_docs/$(basename "$f").txt" 2>/dev/null || true
   done

echo "=== PHASE 4: MERGE CHATS ==="
find "$OUT" -type f -iname '*chat*.txt' -print0 | xargs -0 cat > "$OUT/ENGINE_MEMORY/chat_memory/merged_chats.txt" || true

echo "=== PHASE 5: BUILD MASTER INDEX ==="
python3 - <<'PY'
import os, json, hashlib
root = os.path.abspath(os.getcwd())
index=[]
for dp,_,fs in os.walk(root):
    for f in fs:
        p=os.path.join(dp,f)
        try:
            with open(p,'rb') as fh: h=hashlib.sha256(fh.read()).hexdigest()
            index.append({"path":p.replace(root+"/",""),"sha":h})
        except: pass
with open("ENGINE_CORE/knowledge_bank/MASTER_KNOWLEDGE.json","w") as fh:
    json.dump({"count":len(index),"files":index},fh,indent=2)
PY
echo "=== DONE ==="
