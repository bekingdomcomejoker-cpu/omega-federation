#!/data/data/com.termux/files/usr/bin/env python3
import sqlite3, sys, textwrap

DB = "/data/data/com.termux/files/home/UNIFIED_ENGINE/QUERY_ENGINE/index.db"

def snippet(row, q):
    # simple snippet extractor: find query term, show around it
    path, content = row
    ql = q.lower()
    li = content.lower().find(ql)
    if li == -1:
        return content[:300].replace("\n"," ")[:300]+"..."
    start = max(0, li-120)
    snip = content[start:start+360].replace("\n"," ")
    return "..." + snip.strip() + "..."

def search(q, limit=10):
    c = sqlite3.connect(DB)
    # use FTS5 match syntax; use quote to avoid injection (simple)
    sql = "SELECT path, content FROM docs_fts WHERE docs_fts MATCH ? LIMIT ?"
    # use tokens: add '*' to allow prefix matches
    param = q + "*"
    rows = c.execute(sql, (param, limit)).fetchall()
    if not rows:
        print("No matches.")
        return
    for i, r in enumerate(rows, 1):
        print(f"---[{i}] {r[0]}")
        print(textwrap.fill(snippet(r, q), width=100))
        print()
    c.close()

if __name__ == '__main__':
    if len(sys.argv)<2:
        print("Usage: search.py <query phrase>")
        sys.exit(1)
    q = " ".join(sys.argv[1:])
    search(q, limit=15)
