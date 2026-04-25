"""Unit tests for the indexer that don't need an embedding model."""
from __future__ import annotations

import tempfile
from pathlib import Path

import lancedb

from mybrain_mcp.indexer import (
    TABLE_NAME,
    VECTOR_DIM,
    _table_vector_dim,
    _upsert_rows,
    iter_markdown,
)


def _touch(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# ok\n", encoding="utf-8")


def test_iter_markdown_skips_vendored_dirs():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _touch(root / "notes.md")
        _touch(root / "docs" / "guide.md")
        _touch(root / ".venv" / "lib" / "vendor.md")
        _touch(root / "node_modules" / "pkg" / "README.md")
        _touch(root / ".git" / "HEAD.md")
        _touch(root / "__pycache__" / "cache.md")
        _touch(root / "build" / "artifact.md")

        found = {p.relative_to(root).as_posix() for p in iter_markdown(root)}

        assert found == {"notes.md", "docs/guide.md"}


def test_iter_markdown_excludes_nested_venv():
    """A .venv inside a subproject should still be excluded."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _touch(root / "a" / "keep.md")
        _touch(root / "a" / "subproject" / ".venv" / "drop.md")

        found = {p.relative_to(root).as_posix() for p in iter_markdown(root)}

        assert found == {"a/keep.md"}


def test_iter_markdown_honors_extra_excludes():
    """Caller-supplied excludes compose with the built-in list."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _touch(root / "overview.md")
        _touch(root / "pages" / "p1.md")
        _touch(root / "raw" / "bulk.md")
        _touch(root / "raw" / "nested" / "more.md")

        found = {
            p.relative_to(root).as_posix()
            for p in iter_markdown(root, extra_excludes=("raw",))
        }

        assert found == {"overview.md", "pages/p1.md"}


def test_upsert_auto_migrates_on_vector_dim_change():
    """An index built with a different embedding model must be auto-rebuilt."""
    with tempfile.TemporaryDirectory() as td:
        data_dir = Path(td)
        db = lancedb.connect(str(data_dir / "lancedb"))
        legacy_dim = 384  # old MiniLM
        db.create_table(
            TABLE_NAME,
            data=[{
                "id": "legacy-1",
                "text": "left over from the 384-d spike",
                "path": "/legacy.md",
                "namespace": "legacy",
                "vector": [0.0] * legacy_dim,
            }],
        )
        assert _table_vector_dim(db.open_table(TABLE_NAME)) == legacy_dim

        new_rows = [{
            "id": "fresh-1",
            "text": "current model row",
            "path": "/fresh.md",
            "namespace": "fresh",
            "vector": [0.0] * VECTOR_DIM,
        }]
        _upsert_rows(data_dir, where="namespace = 'fresh'", rows=new_rows)

        db2 = lancedb.connect(str(data_dir / "lancedb"))
        table = db2.open_table(TABLE_NAME)
        rows = table.to_arrow().to_pylist()
        assert [r["id"] for r in rows] == ["fresh-1"], (
            "legacy row should be gone, only the new row should remain"
        )
        assert _table_vector_dim(table) == VECTOR_DIM


def test_upsert_preserves_data_when_dim_matches():
    """Same-dim upserts must not nuke unrelated namespaces."""
    with tempfile.TemporaryDirectory() as td:
        data_dir = Path(td)
        db = lancedb.connect(str(data_dir / "lancedb"))
        db.create_table(
            TABLE_NAME,
            data=[{
                "id": "a-1",
                "text": "alpha",
                "path": "/a.md",
                "namespace": "alpha",
                "vector": [0.0] * VECTOR_DIM,
            }],
        )
        _upsert_rows(
            data_dir,
            where="namespace = 'beta'",
            rows=[{
                "id": "b-1",
                "text": "beta",
                "path": "/b.md",
                "namespace": "beta",
                "vector": [0.0] * VECTOR_DIM,
            }],
        )
        table = lancedb.connect(str(data_dir / "lancedb")).open_table(TABLE_NAME)
        ids = sorted(r["id"] for r in table.to_arrow().to_pylist())
        assert ids == ["a-1", "b-1"]
