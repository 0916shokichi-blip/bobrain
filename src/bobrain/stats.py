"""Read-only inspection helpers for an existing index."""
from __future__ import annotations

from pathlib import Path

import lancedb

from .indexer import TABLE_NAME, _table_exists


def list_namespaces(data_dir: Path) -> list[dict]:
    """Summarize every namespace currently present in the index.

    Each entry: ``{"namespace": str, "chunks": int, "documents": int}``,
    sorted by namespace name. Returns ``[]`` if no index exists yet.
    """
    db_path = data_dir / "lancedb"
    if not db_path.exists():
        return []
    db = lancedb.connect(str(db_path))
    if not _table_exists(db, TABLE_NAME):
        return []

    rows = db.open_table(TABLE_NAME).to_arrow().select(["namespace", "path"]).to_pylist()
    chunks_by_ns: dict[str, int] = {}
    paths_by_ns: dict[str, set[str]] = {}
    for r in rows:
        ns = r["namespace"]
        chunks_by_ns[ns] = chunks_by_ns.get(ns, 0) + 1
        paths_by_ns.setdefault(ns, set()).add(r["path"])

    return [
        {"namespace": ns, "chunks": chunks_by_ns[ns], "documents": len(paths_by_ns[ns])}
        for ns in sorted(chunks_by_ns)
    ]
