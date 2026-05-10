"""MCP stdio server exposing the hybrid search as a tool."""
from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .redact import redact_results
from .sanitize import process_results
from .search import search as do_search
from .stats import list_namespaces as do_list_namespaces

DATA_DIR = Path(os.environ.get("BOBRAIN_DATA", str(Path.home() / ".bobrain")))
REDACT_ENABLED = os.environ.get("BOBRAIN_REDACT", "1") != "0"

mcp = FastMCP("bobrain")


@mcp.tool()
def search_docs(
    query: str,
    top_k: int = 5,
    namespaces: list[str] | None = None,
) -> list[dict]:
    """Hybrid (BM25 + vector) search over locally indexed directories.

    Search results are passed through two defenses before being returned:
    1. PII / secret redaction on the chunk ``text`` field (emails, common
       API key formats, /Users/<name>/ paths). Disable with
       ``BOBRAIN_REDACT=0`` or ``bobrain serve --no-redact``.
    2. Prompt-injection sanitize layer: each ``text`` is wrapped in a
       ``<bobrain-search-result>`` boundary marker, and a synthetic
       ``_warning`` entry is prepended at index 0 if any result contains
       apparent injection markers.

    Args:
        query: Natural language query string.
        top_k: Max number of results.
        namespaces: Optional list of namespaces to restrict the search to.
    """
    raw = do_search(query, DATA_DIR, top_k=top_k, namespaces=namespaces)
    if REDACT_ENABLED:
        raw = redact_results(raw)
    return process_results(raw)


@mcp.tool()
def list_namespaces() -> list[dict]:
    """List every namespace currently in the local index.

    Each entry has ``namespace``, ``chunks`` (indexed chunk count), and
    ``documents`` (distinct source files). Useful for discovering which
    knowledge sources are available before calling ``search_docs`` with a
    ``namespaces`` filter. Returns ``[]`` if nothing has been indexed yet.
    """
    return do_list_namespaces(DATA_DIR)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
