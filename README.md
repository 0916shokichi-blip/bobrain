<div align="center">
  <img src="assets/mnemo.svg" alt="Mnemo — the librarian of your memory" width="120" height="120"/>
  <h1>MyBrain MCP</h1>
  <p><em>Mnemo, the librarian of your memory.</em></p>
</div>

A **local-first multi-source RAG MCP server** — search across multiple Obsidian vaults and the Markdown docs in your code repositories from Claude, Cursor, Claude Desktop, and any other MCP-compatible client.

> Status: **early prototype**. Markdown-only today; PDF and code-AST chunking are on the roadmap. APIs and storage layout may change.

## What it is

MyBrain MCP indexes multiple local directories into a single hybrid search layer (BM25 + dense embeddings, combined via Reciprocal Rank Fusion) and exposes a `search_docs` MCP tool so your AI client can retrieve relevant chunks across **all of your personal knowledge sources at once**.

Unlike existing RAG servers that focus on a single directory tree or require cloud embeddings, MyBrain:

- runs **fully local** with in-process ONNX embeddings (`multilingual-e5-large`)
- supports **multiple independent root directories** with namespace isolation
- ships **Japanese-aware BM25** out of the box (MeCab via `fugashi + unidic-lite`)
- is designed for people whose knowledge lives in **more than one place** — an Obsidian vault and the README/docs folder of every active repo

## Killer use case

Ask your AI:

> "Where did I write about MCP chunking strategies — either in my notes or the code?"

and get a single ranked list spanning your Obsidian vault and your `~/code/` directory, cited by file path.

## Install

Requires Python 3.12+.

```bash
# Recommended: install once, run from anywhere
pipx install mybrain-mcp

# Or run a one-shot without installing (uv 0.5+)
uvx mybrain --help
```

Or clone and develop locally:

```bash
git clone https://github.com/0916shokichi-blip/mybrain-mcp.git
cd mybrain-mcp
uv sync
```

> First indexing run downloads the `multilingual-e5-large` ONNX weights (~2.2 GB) into the fastembed cache. Subsequent runs reuse it.

## Quickstart

```bash
# index a directory under a namespace
mybrain index ~/Documents/notes -n notes

# index a second namespace (they live side by side)
mybrain index ~/code/my-project -n code

# quick CLI search (BM25 + vector hybrid)
mybrain search "how did I chunk markdown" -k 5

# cross-namespace filter
mybrain search "mcp server" --ns notes --ns code

# keep the index live while you edit (Ctrl+C to stop)
mybrain watch ~/Documents/notes -n notes
```

(If you cloned the repo instead of installing, prefix every command with `uv run`.)

## MCP client setup

Point your MCP client at the stdio server. If you installed via `pipx`:

```json
{
  "mcpServers": {
    "mybrain": {
      "command": "mybrain",
      "args": ["serve"]
    }
  }
}
```

Or, from a local clone:

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

- [x] Japanese-aware BM25 via MeCab (fugashi + unidic-lite)
- [x] Upgrade embeddings to `multilingual-e5-large` (query/passage prefix aware)
- [x] Incremental indexing with `watchdog` (`mybrain watch`)
- [x] Indexing progress + per-phase wall times (`scan / embed / db-write / bm25`)
- [ ] PDF chunker via `pymupdf` (dependency already in)
- [ ] Markdown heading-aware chunker (today: fixed character window)
- [ ] Code AST-aware chunker (tree-sitter)
- [ ] LLM Wiki auto-detection (directories containing `CLAUDE.md + log.md + index.md`)
- [ ] Reranker integration (Voyage / Cohere)
- [ ] Pro tier with cloud sync and team sharing

## License

MIT. See [LICENSE](./LICENSE).
