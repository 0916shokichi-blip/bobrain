"""End-to-end test: spawn `mybrain serve` and exercise the MCP protocol.

Runs the server as a stdio subprocess, lists tools, and calls `search_docs`
with a query that should hit the bundled sample corpus. Verifies that at
least one result comes back and that its path points into `sample/`.
"""
from __future__ import annotations

import asyncio
import json
import os
import tempfile
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from mybrain_mcp.indexer import build_index

REPO_ROOT = Path(__file__).resolve().parent.parent
SAMPLE_DIR = REPO_ROOT / "sample"


@pytest.fixture(scope="module")
def indexed_data_dir() -> Path:
    """Build a fresh index of the sample corpus in a temp dir."""
    tmp = Path(tempfile.mkdtemp(prefix="mybrain-mcptest-"))
    n = build_index(SAMPLE_DIR, namespace="sample", data_dir=tmp)
    assert n > 0, "indexing produced no chunks"
    return tmp


async def _run_protocol(data_dir: Path) -> dict:
    env = {**os.environ, "MYBRAIN_DATA": str(data_dir)}
    params = StdioServerParameters(command="uv", args=["run", "mybrain", "serve"], env=env)

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = [t.name for t in tools.tools]
            assert "search_docs" in tool_names, f"expected search_docs in {tool_names}"

            result = await session.call_tool(
                "search_docs", {"query": "MCP とは", "top_k": 3}
            )
            assert not result.isError, f"tool returned error: {result}"
            hits = [json.loads(c.text) for c in result.content]
            return {"tools": tool_names, "result": hits}


def test_search_docs_via_mcp(indexed_data_dir: Path) -> None:
    out = asyncio.run(_run_protocol(indexed_data_dir))
    assert "search_docs" in out["tools"]
    results = out["result"]
    assert isinstance(results, list) and len(results) > 0
    assert any("mcp_basics" in r["path"] for r in results), (
        f"expected mcp_basics.md in top results, got {[r['path'] for r in results]}"
    )
