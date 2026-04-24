"""Typer CLI: index / search / serve."""
from __future__ import annotations

import os
from pathlib import Path

import typer

from .indexer import build_index
from .search import search as do_search

app = typer.Typer(help="MyBrain MCP — local multi-source RAG for Claude, Cursor, and friends")

DEFAULT_DATA_DIR = Path(
    os.environ.get("MYBRAIN_DATA", str(Path.home() / ".mybrain"))
)


@app.command()
def index(
    path: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    namespace: str = typer.Option("default", "--namespace", "-n"),
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data", envvar="MYBRAIN_DATA"),
) -> None:
    n = build_index(path, namespace, data_dir)
    typer.echo(f"indexed {n} chunks (ns='{namespace}') at {data_dir}")


@app.command()
def search(
    query: str,
    top_k: int = typer.Option(5, "--top-k", "-k"),
    namespaces: list[str] = typer.Option(None, "--ns"),
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data", envvar="MYBRAIN_DATA"),
) -> None:
    results = do_search(query, data_dir, top_k=top_k, namespaces=namespaces or None)
    if not results:
        typer.echo("(no results)")
        return
    for i, r in enumerate(results, 1):
        typer.echo(f"[{i}] {r['path']} (ns={r['namespace']} score={r['score']:.4f})")
        typer.echo(f"    {r['text'][:200]}...")


@app.command()
def watch(
    path: Path = typer.Argument(..., exists=True, file_okay=False, dir_okay=True),
    namespace: str = typer.Option("default", "--namespace", "-n"),
    data_dir: Path = typer.Option(DEFAULT_DATA_DIR, "--data", envvar="MYBRAIN_DATA"),
    debounce_ms: int = typer.Option(500, "--debounce-ms"),
) -> None:
    """Keep the index in sync with `path` (Ctrl+C to stop)."""
    from .watcher import watch as do_watch

    typer.echo(f"watching {path} (ns='{namespace}', debounce={debounce_ms}ms) — Ctrl+C to stop")
    do_watch(path, namespace, data_dir, debounce_ms=debounce_ms)


@app.command()
def serve() -> None:
    from .server import main as serve_main

    serve_main()


if __name__ == "__main__":
    app()
