"""MCP stdio server exposing the hybrid search as a tool."""
from __future__ import annotations

import os
from pathlib import Path

# Suppress huggingface_hub telemetry by default — bobrain advertises a
# local-first stance, and a silent phone-home on first model fetch
# contradicts that. Users who want telemetry can override before import.
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

from mcp.server.fastmcp import FastMCP

from .redact import redact_results
from .sanitize import process_results
from .search import search as do_search
from .stats import list_namespaces as do_list_namespaces

DATA_DIR = Path(os.environ.get("BOBRAIN_DATA", str(Path.home() / ".bobrain")))
REDACT_ENABLED = os.environ.get("BOBRAIN_REDACT", "1") != "0"

# Upper bound for LLM-supplied ``top_k``. Search results flow on to an
# LLM that may be acting on injected instructions; an unbounded value
# would let an adversarial prompt request thousands of rows and stall
# the stdio loop. 50 is well above any reasonable retrieval-augmented
# generation budget.
MAX_TOP_K = 50

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
        top_k: Max number of results. Clamped to [1, 50].
        namespaces: Optional list of namespaces to restrict the search to.
    """
    top_k = max(1, min(int(top_k), MAX_TOP_K))
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
