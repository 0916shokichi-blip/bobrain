# MyBrain MCP

A **local-first multi-source RAG MCP server** — search across your Obsidian vaults, Git repositories, and PDF libraries from Claude, Cursor, Claude Desktop, and any other MCP-compatible client.

> Status: **early prototype**. APIs and storage layout may change.

## What it is

MyBrain MCP indexes multiple local directories into a single hybrid search layer (BM25 + dense embeddings, combined via Reciprocal Rank Fusion) and exposes a `search_docs` MCP tool so your AI client can retrieve relevant chunks across **all of your personal knowledge sources at once**.

Unlike existing RAG servers that focus on a single directory tree, a single format (Markdown only, code only), or require cloud embeddings, MyBrain:

- runs **fully local** with in-process ONNX embeddings
- supports **multiple independent root directories** with namespace isolation
- is designed for people whose knowledge lives in **more than one place** (a Vault, a few repos, a folder of PDFs)

## Killer use case

Ask your AI:

> "Where did I write about MCP chunking strategies — either in my notes or the code?"

and get a single ranked list spanning your Obsidian vault and your `~/code/` directory, cited by file path.

## Install

Requires Python 3.12+.

```bash
git clone https://github.com/0916shokichi-blip/mybrain-mcp.git
cd mybrain-mcp
uv sync
```

## Quickstart

```bash
# index a directory under a namespace
uv run mybrain index ~/Documents/notes -n notes

# index a second namespace (they live side by side)
uv run mybrain index ~/code/my-project -n code

# quick CLI search (BM25 + vector hybrid)
uv run mybrain search "how did I chunk markdown" -k 5

# cross-namespace filter
uv run mybrain search "mcp server" --ns notes --ns code
```

## MCP client setup

Point your MCP client at the stdio server:

```json
{
  "mcpServers": {
    "mybrain": {
      "command": "uv",
      "args": ["run", "mybrain", "serve"],
      "cwd": "/absolute/path/to/mybrain-mcp"
    }
  }
}
```

Then from Claude / Cursor / Claude Desktop you can call the `search_docs` tool directly.

## Roadmap

- [ ] Upgrade embeddings to `multilingual-e5-large` / BGE-M3 (currently MiniLM-L12 for spike speed)
- [ ] Japanese-aware BM25 via MeCab (fugashi + unidic-lite)
- [ ] Source-type-aware chunkers (Markdown heading-aware, code AST-aware via tree-sitter, PDF layout-aware via pymupdf)
- [ ] Incremental indexing with `watchdog`
- [ ] LLM Wiki auto-detection (directories containing `CLAUDE.md + log.md + index.md`)
- [ ] Reranker integration (Voyage / Cohere)
- [ ] Pro tier with cloud sync and team sharing

## License

MIT. See [LICENSE](./LICENSE).
