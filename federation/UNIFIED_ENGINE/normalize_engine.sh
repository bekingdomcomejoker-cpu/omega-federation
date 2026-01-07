#!/usr/bin/env bash
set -euo pipefail

SRC="${HOME}/storage/shared/AI-TTE"
OUT="${HOME}/UNIFIED_ENGINE/ENGINE_MEMORY"
LOG="${HOME}/UNIFIED_ENGINE/LOGS/normalize.log"
TMP="$OUT/_tmp"

mkdir -p "$OUT" "$TMP" "$OUT/converted" "$OUT/raw" "$OUT/clean" "$OUT/index"

echo "=== PHASE A: COPY RAW TEXT ===" | tee -a "$LOG"
find "$SRC" -type f \
  \( -iname '*.txt' -o -iname '*.md' -o -iname '*.json' -o -iname '*.py' -o -iname '*.sh' \) \
  -size -20M -print0 \
 | xargs -0 -I{} cp -n "{}" "$OUT/raw/" || true

echo "=== PHASE B: CONVERT DOCX/PDF TO TXT ===" | tee -a "$LOG"
find "$SRC" -type f \
  \( -iname '*.docx' -o -iname '*.pdf' \) \
  -size -15M -print0 \
 | while IFS= read -r -d '' f; do
     base=$(basename "$f")
     out="$OUT/converted/${base}.txt"
     pandoc "$f" -t plain -o "$out" 2>>"$LOG" || echo "fail: $f" >> "$LOG"
   done

echo "=== PHASE C: NORMALIZE ALL TEXT ===" | tee -a "$LOG"
for f in "$OUT/raw"/* "$OUT/converted"/*; do
  [ -f "$f" ] || continue
  clean="$OUT/clean/$(basename "$f").clean.txt"
  sed 's/\r//g' "$f" \
    | sed 's/[ \t]\+/ /g' \
    | sed '/^\s*$/d' \
    > "$clean"
done

echo "=== PHASE D: BUILD MASTER INDEX ===" | tee -a "$LOG"
python3 - <<'PY'
import os, hashlib, json

root = os.path.expanduser("~/UNIFIED_ENGINE/ENGINE_MEMORY/clean")
index = []

for dp,_,fs in os.walk(root):
    for f in fs:
        p=os.path.join(dp,f)
        try:
            with open(p,'rb') as fh:
                h=hashlib.sha256(fh.read()).hexdigest()
            rel=p.replace(root+"/","")
            index.append({"file":rel,"sha":h})
        except:
            pass

with open(os.path.expanduser("~/UNIFIED_ENGINE/ENGINE_MEMORY/index/master_index.json"),"w") as fh:
    json.dump(index,fh,indent=2)
PY

echo "=== PHASE E: GENERATE CROSS-REF MAP ==="
python3 - <<'PY'
import os, json

clean = os.path.expanduser("~/UNIFIED_ENGINE/ENGINE_MEMORY/clean")
xref = {}

for f in os.listdir(clean):
    p=os.path.join(clean,f)
    try:
        with open(p,'r',errors='ignore') as fh:
            txt = fh.read().lower()
        if "engine" in txt: xref.setdefault("engine",[]).append(f)
        if "truth" in txt: xref.setdefault("truth",[]).append(f)
        if "axiom" in txt: xref.setdefault("axiom",[]).append(f)
        if "kernel" in txt: xref.setdefault("kernel",[]).append(f)
        if "chronicle" in txt: xref.setdefault("chronicle",[]).append(f)
    except:
        pass

with open(os.path.expanduser("~/UNIFIED_ENGINE/ENGINE_MEMORY/index/crossref.json"),"w") as fh:
    json.dump(xref,fh,indent=2)
PY

echo "=== NORMALIZATION COMPLETE ===" | tee -a "$LOG"
