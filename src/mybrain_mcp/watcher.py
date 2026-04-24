"""Filesystem watcher: keep the MyBrain index in sync with a live directory."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from .indexer import reindex_file, remove_file

MD_SUFFIX = ".md"


@dataclass
class _PendingEvent:
    action: str  # "reindex" | "remove"
    path: Path


class _Debouncer:
    """Collapse rapid-fire events per-path and flush once quiescent."""

    def __init__(self, delay_s: float, flush: Callable[[dict[Path, _PendingEvent]], None]):
        self._delay = delay_s
        self._flush = flush
        self._pending: dict[Path, _PendingEvent] = {}
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def schedule(self, path: Path, action: str) -> None:
        with self._lock:
            self._pending[path] = _PendingEvent(action=action, path=path)
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self._delay, self._flush_now)
            self._timer.daemon = True
            self._timer.start()

    def _flush_now(self) -> None:
        with self._lock:
            pending = self._pending
            self._pending = {}
            self._timer = None
        if pending:
            self._flush(pending)

    def flush_sync(self) -> None:
        """Cancel the pending timer and flush immediately. Used on shutdown / in tests."""
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
        self._flush_now()


class _MarkdownHandler(FileSystemEventHandler):
    def __init__(self, debouncer: _Debouncer):
        self._debouncer = debouncer

    @staticmethod
    def _is_md(path: str | bytes) -> bool:
        return str(path).endswith(MD_SUFFIX)

    def on_created(self, event):
        if event.is_directory:
            return
        if self._is_md(event.src_path):
            self._debouncer.schedule(Path(event.src_path), "reindex")

    def on_modified(self, event):
        if event.is_directory:
            return
        if self._is_md(event.src_path):
            self._debouncer.schedule(Path(event.src_path), "reindex")

    def on_deleted(self, event):
        if event.is_directory:
            return
        if self._is_md(event.src_path):
            self._debouncer.schedule(Path(event.src_path), "remove")

    def on_moved(self, event):
        if event.is_directory:
            return
        if self._is_md(event.src_path):
            self._debouncer.schedule(Path(event.src_path), "remove")
        if self._is_md(event.dest_path):
            self._debouncer.schedule(Path(event.dest_path), "reindex")


def _apply(namespace: str, data_dir: Path, pending: dict[Path, _PendingEvent]) -> None:
    for path, ev in pending.items():
        try:
            if ev.action == "reindex":
                if path.exists():
                    reindex_file(path, namespace, data_dir)
                else:
                    remove_file(path, data_dir)
            else:
                remove_file(path, data_dir)
        except Exception as e:
            print(f"[watcher] error processing {path}: {e}")


def watch(
    root: Path,
    namespace: str,
    data_dir: Path,
    debounce_ms: int = 500,
    stop_event: threading.Event | None = None,
) -> None:
    """Watch `root` recursively and re-index on changes. Blocks until interrupted.

    If `stop_event` is provided, the loop exits when it is set (useful in tests).
    Otherwise, Ctrl+C is the termination signal.
    """
    root_abs = root.resolve()
    debouncer = _Debouncer(
        delay_s=debounce_ms / 1000.0,
        flush=lambda pending: _apply(namespace, data_dir, pending),
    )
    handler = _MarkdownHandler(debouncer)
    observer = Observer()
    observer.schedule(handler, str(root_abs), recursive=True)
    observer.start()
    try:
        if stop_event is not None:
            stop_event.wait()
        else:
            while True:
                time.sleep(1.0)
    except KeyboardInterrupt:
        pass
    finally:
        observer.stop()
        observer.join()
        debouncer.flush_sync()
