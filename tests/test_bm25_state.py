"""Tests for the JSON-based BM25 state store (replaces pickle)."""
from __future__ import annotations

import json
import pickle
from pathlib import Path

import pytest
from rank_bm25 import BM25Okapi

from bobrain.bm25_state import (
    LEGACY_PICKLE_FILE,
    NEW_STATE_FILE,
    load_state,
    save_state,
)


def _make_state() -> dict:
    """Build a minimal state dict shaped like indexer._rebuild_bm25 output."""
    tokenized = [["hello", "world"], ["foo", "bar"], ["hello", "foo"]]
    bm25 = BM25Okapi(tokenized)
    return {
        "bm25": bm25,
        "ids": ["a", "b", "c"],
        "texts": ["hello world", "foo bar", "hello foo"],
        "paths": ["/x/a.md", "/x/b.md", "/x/c.md"],
        "namespaces": ["ns1", "ns1", "ns2"],
    }


def test_save_load_roundtrip_restores_scores(tmp_path: Path) -> None:
    state = _make_state()
    bm25_before = state["bm25"]
    scores_before = list(bm25_before.get_scores(["hello"]))
    save_state(state, tmp_path)
    assert (tmp_path / NEW_STATE_FILE).exists()
    loaded = load_state(tmp_path)
    scores_after = list(loaded["bm25"].get_scores(["hello"]))
    assert scores_after == scores_before, (
        f"score parity broken after JSON round-trip: {scores_before} != {scores_after}"
    )
    assert loaded["ids"] == state["ids"]
    assert loaded["paths"] == state["paths"]
    assert loaded["namespaces"] == state["namespaces"]
    assert loaded["texts"] == state["texts"]


def test_saved_file_is_plain_json_not_pickle(tmp_path: Path) -> None:
    """The whole point of this module — assert the on-disk format parses as JSON."""
    save_state(_make_state(), tmp_path)
    raw = (tmp_path / NEW_STATE_FILE).read_text(encoding="utf-8")
    payload = json.loads(raw)
    assert payload["version"] == 1
    assert "doc_freqs" in payload
    assert "idf" in payload


def test_save_state_empty_corpus(tmp_path: Path) -> None:
    save_state(
        {"bm25": None, "ids": [], "texts": [], "paths": [], "namespaces": []},
        tmp_path,
    )
    loaded = load_state(tmp_path)
    assert loaded["bm25"] is None
    assert loaded["ids"] == []


def test_load_state_missing_raises(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_state(tmp_path)


def test_load_state_falls_back_to_pickle_with_warning(tmp_path: Path) -> None:
    """Legacy ~/.bobrain/bm25.pkl indices should still load (with warning)."""
    state = _make_state()
    # Pickle the same shape the old indexer wrote.
    legacy_payload = {
        "bm25": state["bm25"],
        "ids": state["ids"],
        "texts": state["texts"],
        "paths": state["paths"],
        "namespaces": state["namespaces"],
    }
    (tmp_path / LEGACY_PICKLE_FILE).write_bytes(pickle.dumps(legacy_payload))
    with pytest.warns(DeprecationWarning, match="legacy pickle"):
        loaded = load_state(tmp_path)
    assert loaded["ids"] == state["ids"]


def test_load_state_prefers_json_over_pickle(tmp_path: Path) -> None:
    """If both exist, the JSON file wins and the pickle path is never read."""
    save_state(_make_state(), tmp_path)
    # Plant something that would crash if pickle.load were invoked
    (tmp_path / LEGACY_PICKLE_FILE).write_bytes(b"not-a-real-pickle")
    loaded = load_state(tmp_path)
    assert loaded["bm25"] is not None
    assert loaded["ids"] == ["a", "b", "c"]


def test_save_state_writes_atomically_via_tmp_rename(tmp_path: Path) -> None:
    """tmp file should not linger after a successful write."""
    save_state(_make_state(), tmp_path)
    assert not (tmp_path / (NEW_STATE_FILE + ".tmp")).exists()
    assert (tmp_path / NEW_STATE_FILE).exists()
