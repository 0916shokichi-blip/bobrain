"""Watcher tests.

Two layers:
  1. Unit test on `_apply` + `_Debouncer` — deterministic, no filesystem events.
  2. One end-to-end smoke test with a real watchdog Observer to confirm
     create / modify / delete events actually fire the indexer.

We index on a tiny 3-file corpus so each embed pass is fast.
"""
from __future__ import annotations

import tempfile
import threading
import time
from pathlib import Path

import lancedb
import pytest

from bobrain.indexer import TABLE_NAME, build_index
from bobrain.search import search as do_search
from bobrain.watcher import _apply, _Debouncer, _PendingEvent, watch


def _rows_for(data_dir: Path, filename: str) -> list[dict]:
    db = lancedb.connect(str(data_dir / "lancedb"))
    table = db.open_table(TABLE_NAME)
    return [
        r for r in table.to_arrow().to_pylist() if Path(r["path"]).name == filename
    ]


def _write(path: Path, body: str) -> None:
    path.write_text(body, encoding="utf-8")


def _paths_in_index(data_dir: Path, query: str) -> set[str]:
    results = do_search(query, data_dir, top_k=20)
    return {Path(r["path"]).name for r in results}


@pytest.fixture()
def corpus():
    """A temp source dir (3 .md files) + a temp data dir with a fresh index."""
    with tempfile.TemporaryDirectory(prefix="bobrain-src-") as src, \
         tempfile.TemporaryDirectory(prefix="bobrain-data-") as data:
        src_dir = Path(src)
        data_dir = Path(data)
        _write(src_dir / "alpha.md", "# alpha\n\nThe MCP protocol is designed for agents.")
        _write(src_dir / "beta.md", "# beta\n\n検索アルゴリズムの話。BM25 と dense retrieval。")
        _write(src_dir / "gamma.md", "# gamma\n\nローカルファースト RAG の設計メモ。")
        build_index(src_dir, namespace="watchtest", data_dir=data_dir)
        yield src_dir, data_dir


def test_apply_reindex_picks_up_new_file(corpus):
    src, data = corpus
    new_file = src / "delta.md"
    _write(new_file, "# delta\n\nwatchdog で差分 re-index できるか確認する。")

    _apply("watchtest", data, {new_file: _PendingEvent("reindex", new_file)})

    paths = _paths_in_index(data, "差分 re-index")
    assert "delta.md" in paths


def test_apply_reindex_updates_existing_file(corpus):
    src, data = corpus
    alpha = src / "alpha.md"
    _write(alpha, "# alpha\n\n全く新しい話題: 量子もつれと観測問題。")

    _apply("watchtest", data, {alpha: _PendingEvent("reindex", alpha)})

    rows = _rows_for(data, "alpha.md")
    assert rows, "alpha.md should still have rows after reindex"
    texts = " ".join(r["text"] for r in rows)
    assert "量子もつれ" in texts, "new content missing"
    assert "MCP protocol" not in texts, "old chunks were not replaced"


def test_apply_remove_drops_file(corpus):
    src, data = corpus
    beta = src / "beta.md"
    beta.unlink()

    _apply("watchtest", data, {beta: _PendingEvent("remove", beta)})

    assert _rows_for(data, "beta.md") == []


def test_debouncer_collapses_rapid_events():
    flushed: list[dict] = []
    d = _Debouncer(delay_s=0.05, flush=lambda pending: flushed.append(dict(pending)))
    p = Path("/tmp/x.md")
    for _ in range(5):
        d.schedule(p, "reindex")
        time.sleep(0.005)
    time.sleep(0.2)
    assert len(flushed) == 1
    assert list(flushed[0].keys()) == [p]


def test_debouncer_last_action_wins():
    flushed: list[dict] = []
    d = _Debouncer(delay_s=0.05, flush=lambda pending: flushed.append(dict(pending)))
    p = Path("/tmp/x.md")
    d.schedule(p, "reindex")
    d.schedule(p, "remove")
    time.sleep(0.15)
    assert flushed[0][p].action == "remove"


def test_watch_end_to_end(corpus):
    """Start a real watcher, drop a new file, verify it gets indexed."""
    src, data = corpus
    stop = threading.Event()
    debounce_ms = 100

    t = threading.Thread(
        target=watch,
        kwargs={
            "root": src,
            "namespace": "watchtest",
            "data_dir": data,
            "debounce_ms": debounce_ms,
            "stop_event": stop,
        },
        daemon=True,
    )
    t.start()

    time.sleep(0.2)  # let Observer spin up
    _write(src / "epsilon.md", "# epsilon\n\nファイル監視のエンドツーエンドテスト用。")

    deadline = time.monotonic() + 10.0
    while time.monotonic() < deadline:
        paths = _paths_in_index(data, "ファイル監視 エンドツーエンド")
        if "epsilon.md" in paths:
            break
        time.sleep(0.2)
    else:
        pytest.fail("watcher never indexed the new file within 10s")

    stop.set()
    t.join(timeout=3.0)
    assert not t.is_alive(), "watcher thread did not shut down"
