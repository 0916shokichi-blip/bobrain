# Changelog

All notable changes to bobrain. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versioning is
[SemVer](https://semver.org/) — pre-1.0, minor bumps may include breaking
schema changes (the LanceDB table auto-migrates when the embedding model
or vector dim changes).

## Unreleased

### Added

- `bobrain --version` flag. Previously the only way to inspect the
  installed version was `python -c "import bobrain; print(bobrain.__version__)"`,
  which is poor UX for a CLI. The flag delegates to
  `bobrain.__version__` (which itself reads `importlib.metadata.version`),
  so it stays in sync with `pyproject.toml` automatically.

## 0.3.0 — 2026-05-19

### Added

- **Hash-aware diff index** for `bobrain index`. The default code path now
  computes a content-hash diff against the existing LanceDB rows and only
  embeds new or changed chunks. A Vault where 20 of 642 markdown files
  changed since the last run now embeds ~3% of the previous workload.
  Unchanged chunks are skipped entirely; the BM25 sidecar is only
  rewritten when the table actually changes.
- `bobrain index --full-rebuild` flag bypasses the diff and re-embeds
  every chunk in the namespace. Use it when the BM25 sidecar may be out
  of sync or a guaranteed-clean rebuild is needed (PR #16).
- `build_index(..., full_rebuild=True)` kwarg for programmatic use.

### Changed

- **Progress feedback now on by default** even in non-TTY environments
  (shell scripts, launchd, Claude Code Bash tool). The previous behavior
  was to silently suppress `tqdm` whenever `stderr.isatty()` was false,
  which made long embed runs indistinguishable from a hung process. Set
  `BOBRAIN_QUIET=1` to opt out (PR #14).
- tqdm reports progress every 5 s (`mininterval=5.0`) so non-TTY callers
  see line-buffered updates instead of nothing until completion.
- `_phase` prints a `starting (N items)…` line before each long phase
  (embed, db-write) so users can see something is happening even before
  the first tqdm update.
- README "First-run cost" table updated to reflect measured throughput
  (~3–6 sec/chunk on Apple Silicon CPU, not the previously documented
  1.4–2.4 sec/chunk). 1,000 chunks now correctly estimated at 60–90
  minutes for the first run; subsequent runs are typically seconds for
  daily-update-sized diffs (PR #17).

### Migration

No breaking changes. Existing `~/.bobrain/lancedb/` indexes are reused;
they just become much cheaper to keep current. The chunk ID format
(`hash_id(path, idx, text)`) is unchanged.

## 0.2.0 — 2026-05-19

### Fixed

- **Fresh-install blocker A**: macOS volatile `/tmp` no longer wipes the
  ~2 GB e5-large weights between reboots. fastembed's cache directory is
  now an explicit `data_dir / "fastembed_cache"` (default
  `~/.bobrain/fastembed_cache/`).
- **Fresh-install blocker B**: pinned `fastembed==0.5.1` so the
  `multilingual-e5-large` ONNX External Data file (`model.onnx_data`,
  ~2.1 GB) downloads correctly. fastembed 0.6+ omits the external-data
  entry from the download manifest and the loader fails at first use.
- `__version__` is now sourced from `importlib.metadata.version("bobrain")`
  so `pyproject.toml` is the single source of truth (no more manual sync).
- CI ignores five `pillow` CVEs that come in via fastembed 0.5.1's
  transitive `pillow<11` pin. bobrain does not import `pillow`; the image
  decoding paths are unreachable.

## 0.1.0 — 2026-04-27

Initial PyPI release. Local-first hybrid RAG MCP server over markdown
sources. Hybrid BM25 + dense (`multilingual-e5-large`) retrieval with a
Japanese tokenizer in the default install. MCP tool: `search_docs`.
