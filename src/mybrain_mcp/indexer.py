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
from rank_bm25 import BM25Okapi

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
VECTOR_DIM = 384
TABLE_NAME = "chunks"


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
    model = TextEmbedding(model_name=MODEL_NAME)
    return [list(map(float, v)) for v in model.embed(texts)]


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


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
    if TABLE_NAME in db.table_names():
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
