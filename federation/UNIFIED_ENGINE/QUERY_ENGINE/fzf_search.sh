#!/data/data/com.termux/files/usr/bin/bash
DB=~/UNIFIED_ENGINE/QUERY_ENGINE/index.db
qry="$*"
if [ -z "$qry" ]; then
  echo "Usage: fzf_search.sh <query>"
  exit 1
fi
sqlite3 -separator $'\t' "$DB" "SELECT path FROM docs_fts WHERE docs_fts MATCH '$(printf %q "$qry")*' LIMIT 200;" \
  | fzf --ansi --preview 'bat --style=numbers --color=always --line-range :300 {}' \
  | xargs -r -I{} sh -c 'echo "---- {} ----"; sed -n "1,200p" "{}"'
