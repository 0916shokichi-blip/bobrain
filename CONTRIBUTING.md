# Contributing

Bobrain is in early prototype phase. Issues, bug reports, and PRs are welcome.

## Local development

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/0916shokichi-blip/bobrain.git
cd bobrain
uv sync
uv run pytest -q          # 16 tests, ~30s on a warm cache
```

The first test run downloads the `multilingual-e5-large` ONNX weights (~2.2 GB) into the fastembed cache. Subsequent runs reuse it.

## Trying your change against a real index

```bash
uv run bobrain index ./your-notes -n notes
uv run bobrain search "some query" -k 5 --ns notes
uv run bobrain serve     # stdio MCP server
```

## What we look for in a PR

- Tests for any new behavior in `tests/` (mirror the structure of `test_indexer.py` / `test_watch.py`)
- No new top-level dependencies unless they pull their weight — the install footprint already includes a multilingual ONNX model
- Follow the patterns in `src/bobrain/` (small modules, pure functions where practical, dataclasses for records)
- Keep the `search_docs` MCP tool surface minimal — additions there affect every downstream client

## Reporting issues

Please include:

- macOS / Linux / Windows version
- Python version (`python --version`)
- A minimal repro: a few `.md` files plus the `bobrain` command(s) you ran
- The full stderr (the indexer prints `scan / embed / db-write / bm25` timings — paste them in)
