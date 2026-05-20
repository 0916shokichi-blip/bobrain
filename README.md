<div align="center">
  <img src="assets/bob.svg" alt="Bob" width="120" height="120"/>
  <h1>Bobrain</h1>
  <p><em>The answer you're searching for — you already wrote it, years ago.</em></p>
  <p>
    <a href="https://github.com/0916shokichi-blip/bobrain/actions/workflows/ci.yml">
      <img src="https://github.com/0916shokichi-blip/bobrain/actions/workflows/ci.yml/badge.svg" alt="CI"/>
    </a>
  </p>
</div>

A **local-first hybrid RAG MCP server** that indexes your Obsidian vault and your Git repos together. Hybrid BM25 + e5 retrieval with a Japanese tokenizer in the default install, MCP-native for Claude, Cursor, Claude Desktop, and any other MCP-compatible client.

> Status: **early prototype**. Markdown-only today; PDF and code-AST chunking are on the roadmap. APIs and storage layout may change.

> Landing page: **<https://0916shokichi-blip.github.io/bobrain/>** — also browsable locally via `python3 -m http.server` from the repo root → `http://localhost:8000/docs/`.

## What it is

Bobrain indexes multiple local directories into a single hybrid search layer (BM25 + dense embeddings, combined via Reciprocal Rank Fusion) and exposes a `search_docs` MCP tool so your AI client can retrieve relevant chunks across **all of your personal knowledge sources at once**.

Unlike existing RAG servers that focus on a single directory tree or require cloud embeddings, Bobrain:

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
pipx install bobrain

# Or run a one-shot without installing (uv 0.5+)
uvx bobrain --help
```


Or clone and develop locally:

```bash
git clone https://github.com/0916shokichi-blip/bobrain.git
cd bobrain
uv sync
```

### First-run cost (set expectations)

| Step | Cost | Notes |
| --- | --- | --- |
| Model download | ~2.2 GB | `multilingual-e5-large` ONNX weights, fetched once into `~/.bobrain/fastembed_cache/` |
| Memory peak | ~12 GB | e5-large runs on CPU (1024-dim, 24-layer). Expect a transient spike during embed |
| Indexing time | ~3–6 sec/chunk | CPU inference, Apple Silicon (sustained loads slow due to thermal throttling). ~1,000 chunks ≈ 60–90 minutes on the first run; **subsequent runs only re-embed changed chunks** (typically seconds for daily updates) |
| Disk after indexing | ~50 MB / 1,000 chunks | LanceDB columnar storage under `~/.bobrain/lancedb/` |

Subsequent `bobrain index` runs reuse the cached weights and use a
content-hash diff to skip unchanged chunks (typically seconds for daily
updates). Pass `--full-rebuild` to force a clean rebuild if the BM25
sidecar might be out of sync.

## Quickstart

The intended path is **MCP client → bobrain → your sources**. Index
once, then ask your AI client in natural language. The CLI shown at the
end is for debugging and scripting.

### 1. Index your sources

```bash
# index a directory under a namespace
bobrain index ~/Documents/notes -n notes

# index a second namespace (they live side by side)
bobrain index ~/code/my-project -n code

# index multiple roots into one namespace in a single pass
bobrain index ~/vault ~/code/my-project -n combined
```

### 2. Connect from your MCP client

Configure Claude Desktop, Cursor, or Claude Code (see
[MCP client setup](#mcp-client-setup) below for the JSON snippets).
Once connected, ask in natural language:

> "How did I think about retry/backoff in any past project?"

Your client calls `search_docs` under the hood and folds the matching
chunks into its reply.

### 3. CLI (debugging / scripting)

The same retrieval is available from the shell:

```bash
# quick CLI search (BM25 + vector hybrid)
bobrain search "how did I chunk markdown" -k 5

# cross-namespace filter
bobrain search "mcp server" --ns notes --ns code

# keep the index live while you edit (Ctrl+C to stop)
bobrain watch ~/Documents/notes -n notes
```

### Excluding files with `.bobrainignore`

Drop a `.bobrainignore` at any indexed root (gitignore syntax) to exclude
private notes, scratch files, or whole subtrees:

```gitignore
# private/
private/
drafts/

# everything ending in .scratch.md
*.scratch.md

# negation re-includes a single file
!drafts/ship-this-one.md
```

Patterns from a `.bobrainignore` apply only inside its own directory subtree
(same semantics as `.gitignore`), so you can place a narrower one in a
subfolder. The built-in skip list (`.venv`, `node_modules`, `.git`, ...) is
always active and cannot be re-enabled via `.bobrainignore`.

(If you cloned the repo instead of installing, prefix every command with `uv run`.)

## MCP client setup

Point your MCP client at the stdio server. If you installed via `pipx`:

```json
{
  "mcpServers": {
    "bobrain": {
      "command": "bobrain",
      "args": ["serve"]
    }
  }
}
```
The `bobrain` command on `PATH` works the same way whether you installed from PyPI or from the git URL above.

Or, from a local clone:

```json
{
  "mcpServers": {
    "bobrain": {
      "command": "uv",
      "args": ["run", "bobrain", "serve"],
      "cwd": "/absolute/path/to/bobrain"
    }
  }
}
```

Then from Claude / Cursor / Claude Desktop you can call the MCP tools directly.

## MCP tools

| Tool | What it does |
| --- | --- |
| `search_docs(query, top_k=5, namespaces=None)` | Hybrid (BM25 + vector) search across the local index. `namespaces` is an optional allow-list. |
| `list_namespaces()` | Lists each indexed namespace with its chunk and document counts. Use it to discover what's available before filtering `search_docs`. |

## Roadmap

- [x] Japanese-aware BM25 via MeCab (fugashi + unidic-lite)
- [x] Upgrade embeddings to `multilingual-e5-large` (query/passage prefix aware)
- [x] Incremental indexing with `watchdog` (`bobrain watch`)
- [x] Indexing progress + per-phase wall times (`scan / embed / db-write / bm25`)
- [x] Multi-root `bobrain index` (combine vault + repo in one namespace)
- [x] `.bobrainignore` (gitignore-style per-project exclusions)
- [ ] PDF chunker via `pymupdf` (dependency already in)
- [ ] Markdown heading-aware chunker (today: fixed character window)
- [ ] Code AST-aware chunker (tree-sitter)
- [ ] LLM Wiki auto-detection (directories containing `CLAUDE.md + log.md + index.md`)
- [ ] Reranker integration (Voyage / Cohere)
- [ ] Pro tier with cloud sync and team sharing

## License

MIT. See [LICENSE](./LICENSE).

---

Made by **Bob** — Avatar by Nano Banana Pro.

This is 1 of 8 tools by Bob. → [other tools](https://github.com/0916shokichi-blip)

---

## 🗂 状態: Fold (資産化して畳まれた)

- **fold 日**: 2026-05-20
- **理由**: target persona (path-forgotten heavy memo user) と作者本人 (path-known user) の zero overlap が dogfooding gate で判明、作者が自分で日常的に使う場面が成立しない
- **回収された価値**: PyPI publish 10 地雷の運用知見 (memory `bobrain_pypi_launch` 蒸留済) + hybrid BM25+e5+LanceDB 設計パターン (本 repo retain) + Phase 2 #14「Claude memory blind spot」アイデア
- **再開条件**: 自分が path 忘れる規模のメモ蓄積を持つ生活構造になる、または target persona からの強い使用報告が発生する

これは **敗北ではなく資産化** です。学習・部分コード・アイデアは別の場所に活きています。
PyPI 0.3.0 と GitHub repo は retain (依存解決経路維持のため archive にしません)。Show HN 投稿は予定なし。
