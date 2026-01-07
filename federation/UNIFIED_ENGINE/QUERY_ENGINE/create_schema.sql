PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

-- documents table (meta)
CREATE TABLE IF NOT EXISTS documents (
  id INTEGER PRIMARY KEY,
  path TEXT UNIQUE,
  mtime INTEGER,
  size INTEGER
);

-- full text search virtual table (FTS5)
CREATE VIRTUAL TABLE IF NOT EXISTS docs_fts USING fts5(
  path UNINDEXED,
  content,
  tokenize = "unicode61"
);
