"""Unit tests for the indexer that don't need an embedding model."""
from __future__ import annotations

import tempfile
from pathlib import Path

import lancedb

from bobrain.indexer import (
    TABLE_NAME,
    VECTOR_DIM,
    _table_vector_dim,
    _upsert_rows,
    build_chunks,
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


def test_bobrainignore_at_root_filters_files():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _touch(root / "keep.md")
        _touch(root / "drafts" / "wip.md")
        _touch(root / "private" / "secret.md")
        _touch(root / "notes" / "private" / "leaked.md")
        (root / ".bobrainignore").write_text(
            "drafts/\nprivate/\n", encoding="utf-8"
        )

        found = {p.relative_to(root).as_posix() for p in iter_markdown(root)}

        assert found == {"keep.md"}


def test_bobrainignore_supports_glob_patterns():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _touch(root / "real.md")
        _touch(root / "scratch.tmp.md")
        _touch(root / "subdir" / "another.tmp.md")
        (root / ".bobrainignore").write_text("*.tmp.md\n", encoding="utf-8")

        found = {p.relative_to(root).as_posix() for p in iter_markdown(root)}

        assert found == {"real.md"}


def test_bobrainignore_negation_re_includes():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _touch(root / "drafts" / "wip.md")
        _touch(root / "drafts" / "ship.md")
        (root / ".bobrainignore").write_text(
            "drafts/*\n!drafts/ship.md\n", encoding="utf-8"
        )

        found = {p.relative_to(root).as_posix() for p in iter_markdown(root)}

        assert found == {"drafts/ship.md"}


def test_bobrainignore_nested_only_affects_subtree():
    """A .bobrainignore inside a subdirectory only filters paths under that dir."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _touch(root / "notes.md")
        _touch(root / "scratch.md")
        _touch(root / "sub" / "scratch.md")
        _touch(root / "sub" / "keep.md")
        (root / "sub" / ".bobrainignore").write_text(
            "scratch.md\n", encoding="utf-8"
        )

        found = {p.relative_to(root).as_posix() for p in iter_markdown(root)}

        assert found == {"notes.md", "scratch.md", "sub/keep.md"}


def test_bobrainignore_inside_excluded_dir_is_ignored():
    """A .bobrainignore buried in .venv/ must not influence indexing."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        _touch(root / "keep.md")
        (root / ".venv").mkdir()
        (root / ".venv" / ".bobrainignore").write_text(
            "keep.md\n", encoding="utf-8"
        )

        found = {p.relative_to(root).as_posix() for p in iter_markdown(root)}

        assert found == {"keep.md"}


def test_build_chunks_accepts_multiple_roots():
    with tempfile.TemporaryDirectory() as td_a, tempfile.TemporaryDirectory() as td_b:
        root_a = Path(td_a)
        root_b = Path(td_b)
        (root_a / "a.md").write_text("# A\nalpha body\n", encoding="utf-8")
        (root_b / "b.md").write_text("# B\nbeta body\n", encoding="utf-8")

        chunks = build_chunks([root_a, root_b], namespace="multi")

        paths = sorted(c.path for c in chunks)
        assert paths == sorted([str(root_a / "a.md"), str(root_b / "b.md")])
        assert all(c.namespace == "multi" for c in chunks)


def test_build_chunks_dedupes_overlapping_roots():
    """If two roots overlap, the same file must be chunked only once."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        (root / "outer.md").write_text("outer", encoding="utf-8")
        (root / "sub").mkdir()
        (root / "sub" / "inner.md").write_text("inner", encoding="utf-8")

        chunks = build_chunks([root, root / "sub"], namespace="dup")

        paths = sorted(c.path for c in chunks)
        assert paths == sorted([str(root / "outer.md"), str(root / "sub" / "inner.md")])


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
