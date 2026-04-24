"""Indexer: markdown → chunks → embeddings → LanceDB + BM25 pickle."""
from __future__ import annotations

import hashlib
import pickle
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import lancedb
from fastembed import TextEmbedding
from fugashi import Tagger
from rank_bm25 import BM25Okapi

MODEL_NAME = "intfloat/multilingual-e5-large"
VECTOR_DIM = 1024
TABLE_NAME = "chunks"

_NOISE_POS = {"助詞", "助動詞", "補助記号", "空白", "記号"}
_tagger: Tagger | None = None


def _get_tagger() -> Tagger:
    global _tagger
    if _tagger is None:
        _tagger = Tagger()
    return _tagger


@dataclass
class Chunk:
    id: str
    text: str
    path: str
    namespace: str


def iter_markdown(root: Path) -> Iterable[Path]:
    return (p for p in root.rglob("*.md") if p.is_file())


def chunk_markdown(text: str, max_chars: int = 1000) -> list[str]:
    sections = re.split(r"\n(?=#{1,6} )", text)
    chunks: list[str] = []
    for s in sections:
        s = s.strip()
        if not s:
            continue
        if len(s) <= max_chars:
            chunks.append(s)
            continue
        buf: list[str] = []
        buf_len = 0
        for para in s.split("\n\n"):
            if buf_len + len(para) > max_chars and buf:
                chunks.append("\n\n".join(buf))
                buf = [para]
                buf_len = len(para)
            else:
                buf.append(para)
                buf_len += len(para) + 2
        if buf:
            chunks.append("\n\n".join(buf))
    return chunks


def hash_id(path: str, idx: int, text: str) -> str:
    h = hashlib.sha256()
    h.update(path.encode())
    h.update(str(idx).encode())
    h.update(text.encode())
    return h.hexdigest()[:16]


def build_chunks(root: Path, namespace: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    for p in iter_markdown(root):
        text = p.read_text(encoding="utf-8", errors="ignore")
        for i, c in enumerate(chunk_markdown(text)):
            chunks.append(Chunk(id=hash_id(str(p), i, c), text=c, path=str(p), namespace=namespace))
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed documents for indexing. Uses passage_embed so e5 prefixes are applied."""
    model = TextEmbedding(model_name=MODEL_NAME)
    return [list(map(float, v)) for v in model.passage_embed(texts)]


def tokenize(text: str) -> list[str]:
    tagger = _get_tagger()
    tokens: list[str] = []
    for w in tagger(text):
        if w.feature.pos1 in _NOISE_POS:
            continue
        lemma = getattr(w.feature, "lemma", None) or w.surface
        lemma = lemma.split("-", 1)[0]
        token = lemma.lower().strip()
        if token:
            tokens.append(token)
    return tokens


def build_index(root: Path, namespace: str, data_dir: Path) -> int:
    data_dir.mkdir(parents=True, exist_ok=True)
    chunks = build_chunks(root, namespace)
    if not chunks:
        return 0

    texts = [c.text for c in chunks]
    vectors = embed_texts(texts)

    db = lancedb.connect(str(data_dir / "lancedb"))
    rows = [
        {
            "id": c.id,
            "text": c.text,
            "path": c.path,
            "namespace": c.namespace,
            "vector": v,
        }
        for c, v in zip(chunks, vectors)
    ]
    if TABLE_NAME in db.list_tables():
        db.drop_table(TABLE_NAME)
    db.create_table(TABLE_NAME, data=rows)

    tokenized = [tokenize(t) for t in texts]
    bm25 = BM25Okapi(tokenized)
    with (data_dir / "bm25.pkl").open("wb") as f:
        pickle.dump(
            {
                "bm25": bm25,
                "ids": [c.id for c in chunks],
                "texts": texts,
                "paths": [c.path for c in chunks],
                "namespaces": [c.namespace for c in chunks],
            },
            f,
        )
    return len(chunks)
