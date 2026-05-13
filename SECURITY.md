# Security Policy

## Reporting a Vulnerability

If you've found a security issue in bobrain, please **do not open a public
issue**. Instead, use one of the private channels below so the bug can be
fixed before it is widely known.

**Preferred — GitHub private vulnerability reporting:**
<https://github.com/0916shokichi-blip/bobrain/security/advisories/new>

If GitHub's flow doesn't work for your case, you can also email the
maintainer at the noreply address shown on recent commits:

```
278669525+0916shokichi-blip@users.noreply.github.com
```

(GitHub forwards mail sent to that address to the account owner.)

### What to include

- A short description of the issue and the impact you believe it has
- Steps to reproduce, or a proof-of-concept
- The bobrain version (`bobrain --version`) and how it was installed
  (`pipx`, `uvx`, source checkout)
- Anything else that helps triage (logs, traces, configs — please
  scrub secrets)

### What to expect

- An acknowledgement within 7 days
- A fix or a clear "won't fix" with reasoning within 30 days for
  high-severity issues; longer for low-severity ones
- Credit in the release notes if you'd like (or anonymous, your call)

This is a single-maintainer project run as a side effort, so timelines
are best-effort, not contractual.

## Supported Versions

bobrain is pre-1.0; only the latest release on PyPI receives security
updates. If you're running an older release, please upgrade before
reporting.

| Version | Supported |
|---------|-----------|
| latest on PyPI | ✅ |
| any older release | ❌ — please upgrade |

## Scope

bobrain is a local-first MCP server. It runs over stdio under the same
OS user as the calling tool (Claude Desktop, Cursor, Claude Code, etc.).
It does not open network listeners, accept inbound HTTP, or talk to
external services for indexing.

**In scope:**

- Code execution paths reachable through indexed content
  (e.g. crafted Markdown, crafted index files in `~/.bobrain/`)
- Indirect prompt injection that gets past the sanitize layer in
  `src/bobrain/sanitize.py`
- PII / secret leakage past the redact layer in `src/bobrain/redact.py`
- Path traversal or symlink follow bugs in `src/bobrain/indexer.py`
- Dependency vulnerabilities flagged by `pip-audit` against the locked
  dependency set (`uv.lock`)

**Out of scope:**

- Issues that require an attacker to already have write access to your
  home directory or the data dir (`BOBRAIN_DATA`, default `~/.bobrain/`).
  At that point, bobrain is the smaller problem.
- Vulnerabilities in the LLM that consumes bobrain's search results
  (Anthropic Claude, OpenAI, etc.) — those belong to the LLM provider.
- MCP client misconfiguration (e.g. an attacker-controlled
  `claude_desktop_config.json` that points `BOBRAIN_DATA` at a malicious
  path). The MCP client itself is the trust boundary there.
- Telemetry / network-egress reports for indexing — bobrain does not
  perform network indexing. Model-download telemetry from
  `huggingface_hub` is suppressed by default in the MCP server entry
  (`HF_HUB_DISABLE_TELEMETRY=1`); we treat re-enabling it on by default
  upstream as a bug worth reporting.

## Defenses in place (as of 2026-05-13)

These are the layers a vulnerability would have to bypass; describing
them helps you target a report and helps us avoid duplicates:

1. **Prompt-injection sanitize layer** (`src/bobrain/sanitize.py`):
   ~20 patterns covering English, Japanese, ChatML, Llama, and Alpaca
   chat-template tags, plus NFKC + zero-width-strip normalization to
   defeat full-width and zero-width bypasses. Search results are
   wrapped in `<bobrain-search-result>` boundary markers, and a
   synthetic warning entry is prepended when any chunk is suspect.
2. **PII / secret redaction layer** (`src/bobrain/redact.py`):
   ~17 patterns covering email, JWT, common API key formats
   (Anthropic, OpenAI, GitHub PAT, GitLab PAT, AWS, Slack, Google,
   Bearer), Unix and Windows user paths, and an env-style fallback.
   Disable with `BOBRAIN_REDACT=0` or `bobrain serve --no-redact` only
   on fully trusted vaults.
3. **No pickle on the read path** (`src/bobrain/bm25_state.py`,
   v0.2.0+): BM25 state is persisted as JSON and rehydrated via
   `__new__` + attribute restore. Legacy pickle files written by
   pre-v0.2.0 builds are still readable for one release with a
   deprecation warning, then removed in v0.3.0.
4. **`top_k` clamp** (`src/bobrain/server.py`): the LLM-supplied
   `top_k` is clamped to `[1, 50]` so a poisoned prompt can't request
   tens of thousands of rows and stall the stdio loop.
5. **Namespace allow-list** (`src/bobrain/indexer.py::validate_namespace`):
   namespaces are restricted to `[A-Za-z0-9_-]{1,64}` before
   interpolation into LanceDB SQL filters. The single-quote escape in
   `_escape_sql` also handles backslashes.
6. **Strict UTF-8 indexing** (`src/bobrain/indexer.py::chunks_for_file`):
   files that fail strict UTF-8 decoding are skipped with a warning
   instead of being silently degraded with `errors="ignore"`, which
   used to leak binary fragments into the index.
7. **Dependency auditing in CI** (`.github/workflows/ci.yml`):
   `pip-audit` runs against `uv.lock` on every push; a new CVE in any
   transitive dependency fails the workflow.

## Past audits

- **2026-05-10** — first-pass review (`/ast-map` + `code-reviewer-ja`)
  surfaced 6 architectural issues. 4 of 6 fixed before launch
  (sanitize, redact, README scope, env-style hardening); 2 deferred
  (search.py refactor, indexer.py split).
- **2026-05-13** — second-pass review (independent
  `code-reviewer-ja` plus self-audit) surfaced 13 issues
  (6 high / 7 medium / 4 watch-only). All 6 high and all 7 medium
  fixed in the same week. The pickle-to-JSON migration above is the
  most user-visible change; the rest are pattern additions and
  defensive normalization.
