"""MCP stdio server exposing the hybrid search as a tool."""
from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .sanitize import process_results
from .search import search as do_search
from .stats import list_namespaces as do_list_namespaces

DATA_DIR = Path(os.environ.get("BOBRAIN_DATA", str(Path.home() / ".bobrain")))

mcp = FastMCP("bobrain")


@mcp.tool()
def search_docs(
    query: str,
    top_k: int = 5,
    namespaces: list[str] | None = None,
) -> list[dict]:
    """Hybrid (BM25 + vector) search over locally indexed directories.

    Each result's ``text`` is wrapped in a ``<bobrain-search-result>`` boundary
    marker so the calling LLM sees indexed content as external data, not
    instructions. When any result contains apparent prompt-injection markers,
    a synthetic ``_warning`` entry is prepended at index 0.

    Args:
        query: Natural language query string.
        top_k: Max number of results.
        namespaces: Optional list of namespaces to restrict the search to.
    """
    raw = do_search(query, DATA_DIR, top_k=top_k, namespaces=namespaces)
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
