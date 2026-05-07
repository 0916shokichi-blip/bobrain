"""Unit tests for the read-only namespace inspection helper."""
from __future__ import annotations

import tempfile
from pathlib import Path

from bobrain.indexer import VECTOR_DIM, _upsert_rows
from bobrain.stats import list_namespaces


def _row(id: str, namespace: str, path: str) -> dict:
    return {
        "id": id,
        "text": f"row {id}",
        "path": path,
        "namespace": namespace,
        "vector": [0.0] * VECTOR_DIM,
    }


def test_list_namespaces_empty_when_no_index():
    with tempfile.TemporaryDirectory() as td:
        assert list_namespaces(Path(td)) == []


def test_list_namespaces_aggregates_chunks_and_documents():
    with tempfile.TemporaryDirectory() as td:
        data_dir = Path(td)
        _upsert_rows(
            data_dir,
            where="namespace = 'notes'",
            rows=[
                _row("n1", "notes", "/notes/a.md"),
                _row("n2", "notes", "/notes/a.md"),
                _row("n3", "notes", "/notes/b.md"),
            ],
        )
        _upsert_rows(
            data_dir,
            where="namespace = 'code'",
            rows=[_row("c1", "code", "/code/x.md")],
        )

        assert list_namespaces(data_dir) == [
            {"namespace": "code", "chunks": 1, "documents": 1},
            {"namespace": "notes", "chunks": 3, "documents": 2},
        ]
