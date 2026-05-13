"""BM25 state persistence as JSON. Replaces the pre-v0.2.0 pickle store.

The legacy pickle path (``~/.bobrain/bm25.pkl``) was an arbitrary-code-
execution risk: anyone who could write to ``~/.bobrain/`` could craft a
``__reduce__`` payload that ran on import. We now serialize BM25Okapi's
plain-data internals (idf, doc_freqs, doc_len, plus scalar tuning
params) as JSON and rebuild the object at load time via ``__new__`` —
no pickle protocol involved.

Backwards compatibility: ``load_state`` still reads the old pickle file
if no JSON state exists, emits a ``DeprecationWarning`` once, and the
next index run replaces it with the JSON store. The pickle fallback
path is scheduled for removal in v0.3.0.
"""
from __future__ import annotations

import json
import warnings
from pathlib import Path

from rank_bm25 import BM25Okapi

NEW_STATE_FILE = "bm25_state.json"
LEGACY_PICKLE_FILE = "bm25.pkl"
SCHEMA_VERSION = 1


def save_state(state: dict, data_dir: Path) -> None:
    """Write BM25 state as JSON. ``state`` keys mirror the pre-migration
    pickle shape: ``bm25, ids, texts, paths, namespaces``.

    Writes atomically via ``<file>.tmp`` + ``replace`` so a crash mid-
    write can't corrupt the existing index.
    """
    bm25: BM25Okapi | None = state.get("bm25")
    payload: dict = {
        "version": SCHEMA_VERSION,
        "ids": state["ids"],
        "texts": state["texts"],
        "paths": state["paths"],
        "namespaces": state["namespaces"],
    }
    if bm25 is None:
        payload["corpus_size"] = 0
    else:
        payload.update(
            {
                "corpus_size": bm25.corpus_size,
                "avgdl": bm25.avgdl,
                "k1": bm25.k1,
                "b": bm25.b,
                "epsilon": bm25.epsilon,
                "average_idf": bm25.average_idf,
                "idf": bm25.idf,
                "doc_freqs": bm25.doc_freqs,
                "doc_len": bm25.doc_len,
            }
        )
    data_dir.mkdir(parents=True, exist_ok=True)
    tmp = data_dir / (NEW_STATE_FILE + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    tmp.replace(data_dir / NEW_STATE_FILE)


def load_state(data_dir: Path) -> dict:
    """Load BM25 state. Prefers the JSON file; falls back to pickle once
    with a deprecation warning so existing v0.1.x indices keep working.

    Raises ``FileNotFoundError`` if neither store exists.
    """
    json_path = data_dir / NEW_STATE_FILE
    if json_path.exists():
        return _load_from_json(json_path)

    legacy_path = data_dir / LEGACY_PICKLE_FILE
    if legacy_path.exists():
        return _load_from_legacy_pickle(legacy_path)

    raise FileNotFoundError(
        f"no BM25 state found at {data_dir} (run `bobrain index` to build one)"
    )


def _load_from_json(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    bm25 = _rehydrate_bm25(payload)
    return {
        "bm25": bm25,
        "ids": payload["ids"],
        "texts": payload["texts"],
        "paths": payload["paths"],
        "namespaces": payload["namespaces"],
    }


def _rehydrate_bm25(payload: dict) -> BM25Okapi | None:
    """Restore a BM25Okapi from saved fields without re-fitting the corpus.

    Bypasses ``__init__`` (which would re-tokenize and re-fit) and
    instead restores the previously-computed attributes directly. Safe
    because the source corpus was already tokenized at save time and
    the only state BM25Okapi needs at query time is what we stored.
    """
    if payload.get("corpus_size", 0) == 0:
        return None
    bm25 = BM25Okapi.__new__(BM25Okapi)
    bm25.corpus_size = payload["corpus_size"]
    bm25.avgdl = payload["avgdl"]
    bm25.k1 = payload["k1"]
    bm25.b = payload["b"]
    bm25.epsilon = payload["epsilon"]
    bm25.average_idf = payload["average_idf"]
    bm25.idf = payload["idf"]
    bm25.doc_freqs = payload["doc_freqs"]
    bm25.doc_len = payload["doc_len"]
    bm25.tokenizer = None
    return bm25


def _load_from_legacy_pickle(path: Path) -> dict:
    import pickle  # noqa: S403 — gated deprecation path only

    warnings.warn(
        f"bobrain: {path} is a legacy pickle-format index and will stop "
        f"being read in v0.3.0. Run `bobrain index <root> -n <namespace>` "
        f"to rewrite it as {NEW_STATE_FILE}. The pickle format had an "
        f"arbitrary-code-execution risk if the data dir was writable by "
        f"another process.",
        DeprecationWarning,
        stacklevel=3,
    )
    with path.open("rb") as f:
        return pickle.load(f)  # noqa: S301 — gated deprecation path only
