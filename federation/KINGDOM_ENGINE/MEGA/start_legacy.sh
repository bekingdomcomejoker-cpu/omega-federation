#!/data/data/com.termux/files/usr/bin/bash
BASE="$HOME/KINGDOM_ENGINE/MEGA"
WRAPPER="$BASE/bin/legacy_wrapper.sh"
MANIFEST="$BASE/legacy_manifest.txt"

mkdir -p "$BASE/logs" "$BASE/run"

while IFS= read -r line; do
  # ignore comments/blank
  [ -z "$line" ] && continue
  case "$line" in \#*) continue ;; esac

  path="${line%%||*}"
  friendly="${line#*||}"
  if [ -f "$path" ]; then
    nohup "$WRAPPER" "$path" "$friendly" >/dev/null 2>&1 &
    echo "launched legacy: $friendly ($path)"
  else
    echo "legacy missing: $path (skipped)" >> "$BASE/logs/supervisor.log"
  fi
done < "$MANIFEST"
