"""PII / secret redaction at the server response boundary.

Local-first means the user's Vault never leaves the machine for indexing,
but search results flow on to whatever LLM is calling the MCP tool. This
layer scans result text for common secret formats and user-path patterns,
replacing matches with ``[REDACTED:<type>]`` tokens before the response
goes back.

Heuristic, not a guarantee. Only the chunk ``text`` is redacted — the
``path`` field is bobrain's own metadata (used for click-to-open UX) and
flows through unchanged. Set ``BOBRAIN_REDACT=0`` (or pass ``--no-redact``
to ``bobrain serve``) to disable on fully trusted Vaults.
"""
from __future__ import annotations

import re

# Patterns are applied in order. Email is first so that an address like
# user@host.com isn't shadowed by anything else. Specific high-entropy
# token formats run before the generic ``sk-*`` catch-all so the matched
# region is exactly right (and so later additions can carry distinct
# type labels without reordering). The "/Users/" and "/home/" patterns
# intentionally redact only the username segment so that the rest of
# the path (which often contains useful project context) is preserved
# for the LLM. The env-style fallback runs last to catch leaked
# ``KEY=value`` lines that no specific pattern recognized.
_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\b[\w.+\-]+@[\w\-]+\.[\w.\-]+\b"), "[REDACTED:email]"),
    # JWT (three base64url segments, distinctive eyJ prefix from {"alg")
    (
        re.compile(r"\beyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+"),
        "[REDACTED:jwt]",
    ),
    # Anthropic / OpenAI Project keys (longer and structurally distinct
    # from the legacy sk-* form; redact first so type-specific patterns
    # can be added later without reordering).
    (re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b"), "[REDACTED:api_key]"),
    (re.compile(r"\bsk-proj-[A-Za-z0-9_\-]{20,}\b"), "[REDACTED:api_key]"),
    # GitHub fine-grained PAT and GitLab PAT
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{30,}\b"), "[REDACTED:api_key]"),
    (re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}\b"), "[REDACTED:api_key]"),
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b"), "[REDACTED:api_key]"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "[REDACTED:api_key]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"), "[REDACTED:api_key]"),
    (re.compile(r"\bya29\.[A-Za-z0-9_\-]{20,}\b"), "[REDACTED:api_key]"),
    (re.compile(r"\bxox[bpsa]-[A-Za-z0-9\-]{12,}\b"), "[REDACTED:api_key]"),
    (
        re.compile(r"\bBearer\s+[A-Za-z0-9_.\-+/=]{8,}", re.IGNORECASE),
        "Bearer [REDACTED:api_key]",
    ),
    (re.compile(r"/Users/[^/\s\[]+"), "/Users/[REDACTED:user_path]"),
    (re.compile(r"/home/[^/\s\[]+"), "/home/[REDACTED:user_path]"),
    # Windows user path: C:\Users\<name> (also covers other drive letters)
    (
        re.compile(r"\b([A-Za-z]:\\Users\\)[^\\\s\[/]+"),
        r"\1[REDACTED:user_path]",
    ),
    # env-style fallback. The prefix is optional so bare ``PASSWORD=`` and
    # namespaced ``OPENAI_API_KEY=`` both match. Negative lookahead skips
    # already-redacted values so we don't double-process e.g.
    # ``OPENAI_KEY=[REDACTED:api_key]``.
    (
        re.compile(
            r"(?i)\b((?:[A-Za-z_][A-Za-z0-9_]*)?"
            r"(?:password|passwd|secret|token|api[_-]?key|access[_-]?key|key))"
            r"\s*=\s*['\"]?(?!\[REDACTED)[^\s'\"]{8,}"
        ),
        r"\1=[REDACTED:secret]",
    ),
]


def redact_text(text: str) -> str:
    """Apply every redaction pattern to ``text`` and return the result."""
    if not text:
        return text
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def redact_results(results: list[dict]) -> list[dict]:
    """Return a new list where each row's ``text`` field has been redacted.

    The input list is not mutated. Other fields, including ``path``, pass
    through unchanged so click-to-open UX is preserved.
    """
    return [{**row, "text": redact_text(row.get("text", ""))} for row in results]
