"""MCP stdio server exposing the hybrid search as a tool."""
from __future__ import annotations

import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

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

    Args:
        query: Natural language query string.
        top_k: Max number of results.
        namespaces: Optional list of namespaces to restrict the search to.
    """
    return do_search(query, DATA_DIR, top_k=top_k, namespaces=namespaces)


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
