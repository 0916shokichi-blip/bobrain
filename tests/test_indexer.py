"""Unit tests for the indexer.

Most tests here are pure-logic (no model load). The diff-index tests at
the bottom build a tiny 3-file corpus and call ``build_index`` end-to-end
so they exercise the real fastembed path — same as ``test_watch.py``.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import lancedb

import bobrain.indexer as _indexer
from bobrain.indexer import (
    TABLE_NAME,
    VECTOR_DIM,
    _existing_chunk_ids_for_namespace,
    _table_vector_dim,
    _upsert_rows,
    build_chunks,
    build_index,
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


# --- diff-index tests (real embed, slow) ---


def _write_corpus(src: Path) -> None:
    (src / "alpha.md").write_text(
        "# alpha\n\nThe MCP protocol is designed for agents.", encoding="utf-8"
    )
    (src / "beta.md").write_text(
        "# beta\n\n検索アルゴリズムの話。BM25 と dense retrieval。",
        encoding="utf-8",
    )
    (src / "gamma.md").write_text(
        "# gamma\n\nローカルファースト RAG の設計メモ。", encoding="utf-8"
    )


def test_build_index_is_idempotent_on_rerun():
    """A second build with no source changes must not alter the row set."""
    with tempfile.TemporaryDirectory(prefix="bobrain-src-") as src, \
         tempfile.TemporaryDirectory(prefix="bobrain-data-") as data:
        src_dir = Path(src)
        data_dir = Path(data)
        _write_corpus(src_dir)

        build_index(src_dir, namespace="diff", data_dir=data_dir)
        db = lancedb.connect(str(data_dir / "lancedb"))
        ids_before = {
            r["id"]
            for r in db.open_table(TABLE_NAME).to_arrow().to_pylist()
            if r["namespace"] == "diff"
        }

        build_index(src_dir, namespace="diff", data_dir=data_dir)
        db2 = lancedb.connect(str(data_dir / "lancedb"))
        ids_after = {
            r["id"]
            for r in db2.open_table(TABLE_NAME).to_arrow().to_pylist()
            if r["namespace"] == "diff"
        }

        assert ids_before == ids_after, "idempotent rerun should not change IDs"
        assert ids_before, "corpus should produce at least one chunk"


def test_build_index_skips_embedding_unchanged_chunks(monkeypatch):
    """The diff path must not invoke embed_texts when nothing has changed."""
    with tempfile.TemporaryDirectory(prefix="bobrain-src-") as src, \
         tempfile.TemporaryDirectory(prefix="bobrain-data-") as data:
        src_dir = Path(src)
        data_dir = Path(data)
        _write_corpus(src_dir)

        # First build does real embedding to populate the table.
        build_index(src_dir, namespace="diff", data_dir=data_dir)

        # Spy on the second build: if diff works, embed_texts is never called.
        calls: list[int] = []
        real_embed = _indexer.embed_texts

        def spy(texts, data_dir=None):
            calls.append(len(texts))
            return real_embed(texts, data_dir=data_dir)

        monkeypatch.setattr(_indexer, "embed_texts", spy)
        build_index(src_dir, namespace="diff", data_dir=data_dir)

        assert calls == [], (
            f"unchanged corpus should not trigger embedding, got {calls}"
        )


def test_build_index_only_embeds_added_chunks_after_file_add(monkeypatch):
    """Adding a single new file must embed only that file's chunks."""
    with tempfile.TemporaryDirectory(prefix="bobrain-src-") as src, \
         tempfile.TemporaryDirectory(prefix="bobrain-data-") as data:
        src_dir = Path(src)
        data_dir = Path(data)
        _write_corpus(src_dir)
        build_index(src_dir, namespace="diff", data_dir=data_dir)

        existing_ids = _existing_chunk_ids_for_namespace(data_dir, "diff")

        # Add a new file with content that produces exactly one chunk.
        (src_dir / "delta.md").write_text(
            "# delta\n\njust one chunk worth of body.", encoding="utf-8"
        )

        captured_batches: list[list[str]] = []
        real_embed = _indexer.embed_texts

        def spy(texts, data_dir=None):
            captured_batches.append(list(texts))
            return real_embed(texts, data_dir=data_dir)

        monkeypatch.setattr(_indexer, "embed_texts", spy)
        build_index(src_dir, namespace="diff", data_dir=data_dir)

        # Exactly one embed batch, containing only delta.md text.
        assert len(captured_batches) == 1, (
            f"expected one embed batch, got {len(captured_batches)}"
        )
        assert len(captured_batches[0]) == 1
        assert "just one chunk" in captured_batches[0][0]

        # Final state: previous IDs preserved, one new ID added.
        ids_after = _existing_chunk_ids_for_namespace(data_dir, "diff")
        assert existing_ids.issubset(ids_after)
        assert len(ids_after) == len(existing_ids) + 1


def test_build_index_removes_chunks_when_file_disappears(monkeypatch):
    """Deleting a source file must drop its chunks without re-embedding."""
    with tempfile.TemporaryDirectory(prefix="bobrain-src-") as src, \
         tempfile.TemporaryDirectory(prefix="bobrain-data-") as data:
        src_dir = Path(src)
        data_dir = Path(data)
        _write_corpus(src_dir)
        build_index(src_dir, namespace="diff", data_dir=data_dir)

        ids_before = _existing_chunk_ids_for_namespace(data_dir, "diff")
        (src_dir / "beta.md").unlink()

        calls: list[int] = []
        real_embed = _indexer.embed_texts

        def spy(texts, data_dir=None):
            calls.append(len(texts))
            return real_embed(texts, data_dir=data_dir)

        monkeypatch.setattr(_indexer, "embed_texts", spy)
        build_index(src_dir, namespace="diff", data_dir=data_dir)

        assert calls == [], "deletions alone should not invoke embed_texts"

        ids_after = _existing_chunk_ids_for_namespace(data_dir, "diff")
        assert ids_after.issubset(ids_before)
        assert len(ids_after) < len(ids_before)

        # Verify the rows for beta.md are actually gone.
        table = lancedb.connect(str(data_dir / "lancedb")).open_table(TABLE_NAME)
        beta_rows = [
            r
            for r in table.to_arrow().to_pylist()
            if Path(r["path"]).name == "beta.md"
        ]
        assert beta_rows == []


def test_build_index_full_rebuild_reembeds_everything(monkeypatch):
    """`full_rebuild=True` must re-embed every chunk even when nothing changed."""
    with tempfile.TemporaryDirectory(prefix="bobrain-src-") as src, \
         tempfile.TemporaryDirectory(prefix="bobrain-data-") as data:
        src_dir = Path(src)
        data_dir = Path(data)
        _write_corpus(src_dir)

        build_index(src_dir, namespace="diff", data_dir=data_dir)
        chunk_count = len(_existing_chunk_ids_for_namespace(data_dir, "diff"))
        assert chunk_count >= 3, "corpus should produce at least three chunks"

        # On a forced rebuild the spy should see exactly chunk_count texts
        # passed to embed_texts — proof we bypassed the diff shortcut.
        captured: list[int] = []
        real_embed = _indexer.embed_texts

        def spy(texts, data_dir=None):
            captured.append(len(texts))
            return real_embed(texts, data_dir=data_dir)

        monkeypatch.setattr(_indexer, "embed_texts", spy)
        build_index(
            src_dir,
            namespace="diff",
            data_dir=data_dir,
            full_rebuild=True,
        )

        assert captured == [chunk_count], (
            f"full_rebuild should re-embed every chunk ({chunk_count}), got {captured}"
        )
        # Final id set still matches the corpus content (chunks are
        # deterministic from text), so it's the same set as before.
        ids_after = _existing_chunk_ids_for_namespace(data_dir, "diff")
        assert len(ids_after) == chunk_count
