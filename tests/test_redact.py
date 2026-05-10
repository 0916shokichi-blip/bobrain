"""Tests for the PII / secret redaction layer."""
from __future__ import annotations

import pytest

from bobrain.redact import redact_results, redact_text


# (raw, expected substring in redacted output)
SECRETS = [
    ("contact me at jane.doe@example.com please", "[REDACTED:email]"),
    ("OPENAI_KEY=sk-abc123def456ghi789xyz0", "[REDACTED:api_key]"),
    ("aws_access_key=AKIAIOSFODNN7EXAMPLE", "[REDACTED:api_key]"),
    ("token ghp_1234567890abcdefghijklmnopqrstuv1234", "[REDACTED:api_key]"),
    ("oauth ya29.a0AfH6SMBxxxxxxxxxxxxxxxxxxxxxxxx", "[REDACTED:api_key]"),
    ("slack xoxb-1234567890-1234567890-abcdefghij", "[REDACTED:api_key]"),
    ("Authorization: Bearer abcdefghij1234567890", "Bearer [REDACTED:api_key]"),
    ("path /Users/jane/Documents/notes.md", "/Users/[REDACTED:user_path]/Documents"),
    ("Linux path /home/john/repo/src/main.py", "/home/[REDACTED:user_path]/repo"),
]

BENIGN = [
    "BM25 + vector RRF gives strong recall on Japanese queries.",
    "use sk- prefix for OpenAI API keys",  # bare 'sk-' is too short to match
    "the gh_path string here is unrelated to a token",  # gh_ alone doesn't match ghp_/gho_/...
    "system call: subprocess.run(['ls', '-la'])",
    "/etc/passwd is a system file",  # not under /Users/ or /home/
    "BM25Okapi is a class name",  # alphanumerics that might look like a key
]


@pytest.mark.parametrize("raw,expected_token", SECRETS)
def test_redact_text_masks_known_secrets(raw: str, expected_token: str) -> None:
    out = redact_text(raw)
    assert expected_token in out, f"missed redaction in: {raw!r} → {out!r}"


@pytest.mark.parametrize("text", BENIGN)
def test_redact_text_does_not_mask_benign(text: str) -> None:
    out = redact_text(text)
    assert "[REDACTED" not in out, f"false positive on: {text!r} → {out!r}"


def test_redact_text_handles_empty() -> None:
    assert redact_text("") == ""


def test_redact_text_preserves_path_structure() -> None:
    text = "Read /Users/jane/projects/bobrain/README.md for details"
    out = redact_text(text)
    assert "jane" not in out
    assert "/projects/bobrain/README.md" in out
    assert out.count("[REDACTED:user_path]") == 1


def test_redact_text_handles_multiple_secrets() -> None:
    text = (
        "email foo@bar.com, "
        "key sk-abc123def456ghi789xyz0, "
        "path /Users/x/y"
    )
    out = redact_text(text)
    assert "foo@bar.com" not in out
    assert "sk-abc123" not in out
    assert "/Users/x" not in out
    assert "[REDACTED:email]" in out
    assert "[REDACTED:api_key]" in out
    assert "[REDACTED:user_path]" in out


def test_redact_text_is_idempotent() -> None:
    """Running redact twice should not double-mask the [REDACTED:...] tokens."""
    once = redact_text("/Users/jane/file.md")
    twice = redact_text(once)
    assert once == twice


def test_redact_results_redacts_text_field() -> None:
    rows = [
        {
            "id": "1",
            "path": "/a.md",
            "namespace": "ns",
            "text": "key=sk-1234567890abcdefghij1234",
            "score": 0.9,
        },
    ]
    out = redact_results(rows)
    assert "[REDACTED:api_key]" in out[0]["text"]
    assert out[0]["id"] == "1"
    assert out[0]["score"] == 0.9


def test_redact_results_does_not_mutate_input() -> None:
    rows = [{"id": "1", "text": "ya29.AbCdEfGhIjKlMnOpQrStUvWxYz123456", "score": 0.5}]
    snapshot = [dict(r) for r in rows]
    redact_results(rows)
    assert rows == snapshot


def test_redact_results_does_not_redact_path_field() -> None:
    """``path`` is bobrain's own click-to-open metadata; only ``text`` is sensitive."""
    rows = [
        {"id": "1", "path": "/Users/jane/file.md", "text": "content", "score": 0.5},
    ]
    out = redact_results(rows)
    assert out[0]["path"] == "/Users/jane/file.md"


def test_redact_results_handles_empty_text_field() -> None:
    rows = [{"id": "1", "path": "/a.md", "text": "", "score": 0.5}]
    out = redact_results(rows)
    assert out[0]["text"] == ""


def test_redact_results_handles_empty_input() -> None:
    assert redact_results([]) == []
