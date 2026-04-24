"""Unit tests for the MeCab-backed tokenizer."""
from __future__ import annotations

from mybrain_mcp.indexer import tokenize


def test_japanese_splits_content_words() -> None:
    tokens = tokenize("MCP は LLM と外部のデータを繋ぐオープン標準。")
    assert "mcp" in tokens
    assert "llm" in tokens
    assert "データ" in tokens
    assert "繋ぐ" in tokens
    assert "は" not in tokens
    assert "。" not in tokens


def test_english_passes_through() -> None:
    tokens = tokenize("what is Retrieval Augmented Generation")
    assert tokens == ["what", "is", "retrieval", "augmented", "generation"]


def test_query_matches_conjugated_verb() -> None:
    """BM25 can match a query against conjugated forms via lemma."""
    q = tokenize("繋ぐ")
    doc = tokenize("MCP は LLM と外部を繋いだ。")
    assert set(q).issubset(set(doc)), f"{q} not in {doc}"


def test_katakana_lemma_has_no_english_suffix() -> None:
    """unidic-lite emits 'データ-data' as lemma; we strip the suffix."""
    tokens = tokenize("データ ツール オープン")
    assert "データ" in tokens
    assert "データ-data" not in tokens
    assert "ツール" in tokens
    assert "オープン" in tokens
