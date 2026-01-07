#!/data/data/com.termux/files/usr/bin/env python3
import os, sqlite3, time, hashlib, sys, json
from pathlib import Path
from tqdm import tqdm

HOME = os.path.expanduser("~/UNIFIED_ENGINE")
DB = os.path.expanduser("~/UNIFIED_ENGINE/QUERY_ENGINE/index.db")
# folders to scan (adjust to your structure)
SCAN_PATHS = [
    os.path.expanduser("~/UNIFIED_ENGINE"),
    os.path.expanduser("~/UNIFIED_ENGINE/UNIFIED_ENGINE_MERGE"),
    os.path.expanduser("~/storage/shared"),
    os.path.expanduser("~/UNIFIED_ENGINE/OPTIMIZER")
]

# file patterns to include
INCLUDE_EXT = (".txt", ".md", ".json", ".log", ".py", ".sh", ".cfg", ".ini")

def read_text(path):
    try:
        b = path.read_bytes()
        # try decode utf-8, fallback latin1
        try:
            return b.decode("utf-8", errors="replace")
        except:
            return b.decode("latin-1", errors="replace")
    except:
        return ""

def connect_db():
    c = sqlite3.connect(DB, timeout=30)
    c.execute("PRAGMA journal_mode=WAL;")
    return c

def ensure_tables(c):
    # documents and docs_fts created by create_schema.sql earlier,
    # but ensure exists if user skipped that step
    c.execute("CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, path TEXT UNIQUE, mtime INTEGER, size INTEGER)")
    c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(path UNINDEXED, content, tokenize = 'unicode61')")
    c.commit()

def file_listing():
    for base in SCAN_PATHS:
        if not os.path.isdir(base):
            continue
        for root, dirs, files in os.walk(base):
            # avoid node_modules/.git/tmp heavy directories if present
            if ".git" in root or "node_modules" in root:
                continue
            for f in files:
                if f.lower().endswith(INCLUDE_EXT):
                    yield Path(root) / f

def build_index():
    c = connect_db()
    ensure_tables(c)
    cur = c.cursor()

    # load known docs mapping
    cur.execute("SELECT path, mtime, size FROM documents")
    known = {row[0]: (row[1], row[2]) for row in cur.fetchall()}

    to_process = []
    for p in file_listing():
        try:
            st = p.stat()
        except:
            continue
        mtime = int(st.st_mtime)
        size = st.st_size
        path_str = str(p)
        if path_str in known and known[path_str] == (mtime, size):
            continue
        to_process.append((p, mtime, size))

    for p, mtime, size in tqdm(to_process, desc="Indexing"):
        content = read_text(p)
        if not content.strip():
            # if empty, remove from FTS & documents
            cur.execute("DELETE FROM docs_fts WHERE path = ?", (str(p),))
            cur.execute("DELETE FROM documents WHERE path = ?", (str(p),))
            c.commit()
            continue
        # upsert docs_fts: remove old and add new (simpler than FTS incremental)
        cur.execute("DELETE FROM docs_fts WHERE path = ?", (str(p),))
        cur.execute("INSERT INTO docs_fts (path, content) VALUES (?, ?)", (str(p), content[:2000000]))  # limit huge files
        cur.execute("INSERT OR REPLACE INTO documents (path, mtime, size) VALUES (?, ?, ?)", (str(p), mtime, size))
        c.commit()

    # optionally remove documents that no longer exist
    cur.execute("SELECT path FROM documents")
    for (path,) in cur.fetchall():
        if not os.path.exists(path):
            cur.execute("DELETE FROM documents WHERE path = ?", (path,))
            cur.execute("DELETE FROM docs_fts WHERE path = ?", (path,))
    c.commit()
    c.close()
    print("Index complete. Processed:", len(to_process))

if __name__ == '__main__':
    start = time.time()
    build_index()
    print("Elapsed:", time.time() - start)
