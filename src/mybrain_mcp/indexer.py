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
        chunks.extend(chunks_for_file(p, namespace))
    return chunks


def chunks_for_file(file_path: Path, namespace: str) -> list[Chunk]:
    text = file_path.read_text(encoding="utf-8", errors="ignore")
    return [
        Chunk(
            id=hash_id(str(file_path), i, c),
            text=c,
            path=str(file_path),
            namespace=namespace,
        )
        for i, c in enumerate(chunk_markdown(text))
    ]


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


def _chunks_to_rows(chunks: list[Chunk]) -> list[dict]:
    if not chunks:
        return []
    texts = [c.text for c in chunks]
    vectors = embed_texts(texts)
    return [
        {
            "id": c.id,
            "text": c.text,
            "path": c.path,
            "namespace": c.namespace,
            "vector": v,
        }
        for c, v in zip(chunks, vectors)
    ]


def _rebuild_bm25(table, data_dir: Path) -> None:
    """Re-dump the BM25 pickle from every row currently in the LanceDB table."""
    arrow_table = table.to_arrow().select(["id", "text", "path", "namespace"])
    records = arrow_table.to_pylist()
    texts = [r["text"] for r in records]
    tokenized = [tokenize(t) for t in texts]
    bm25 = BM25Okapi(tokenized) if tokenized else None
    with (data_dir / "bm25.pkl").open("wb") as f:
        pickle.dump(
            {
                "bm25": bm25,
                "ids": [r["id"] for r in records],
                "texts": texts,
                "paths": [r["path"] for r in records],
                "namespaces": [r["namespace"] for r in records],
            },
            f,
        )


def _table_exists(db, name: str) -> bool:
    # LanceDB >= 0.30 returns a ListTablesResponse(tables=[...]) wrapper,
    # so `name in db.list_tables()` is always False. Use `.tables`.
    return name in db.list_tables().tables


def _upsert_rows(data_dir: Path, where: str, rows: list[dict]):
    """Delete existing rows matching `where`, then insert `rows`. Returns the table."""
    data_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(data_dir / "lancedb"))
    if _table_exists(db, TABLE_NAME):
        table = db.open_table(TABLE_NAME)
        table.delete(where)
        if rows:
            table.add(rows)
    elif rows:
        table = db.create_table(TABLE_NAME, data=rows)
    else:
        return None
    return table


def _escape_sql(value: str) -> str:
    return value.replace("'", "''")


def build_index(root: Path, namespace: str, data_dir: Path) -> int:
    """Re-index all markdown under `root` for `namespace` (other namespaces untouched)."""
    chunks = build_chunks(root, namespace)
    rows = _chunks_to_rows(chunks)
    table = _upsert_rows(
        data_dir,
        where=f"namespace = '{_escape_sql(namespace)}'",
        rows=rows,
    )
    if table is None:
        return 0
    _rebuild_bm25(table, data_dir)
    return len(chunks)


def reindex_file(file_path: Path, namespace: str, data_dir: Path) -> int:
    """Re-index a single file. Existing rows for that path (any namespace) are replaced."""
    chunks = chunks_for_file(file_path, namespace)
    rows = _chunks_to_rows(chunks)
    table = _upsert_rows(
        data_dir,
        where=f"path = '{_escape_sql(str(file_path))}'",
        rows=rows,
    )
    if table is None:
        return 0
    _rebuild_bm25(table, data_dir)
    return len(chunks)


def remove_file(file_path: Path, data_dir: Path) -> None:
    """Drop all chunks for a deleted file and rebuild the BM25 pickle."""
    db = lancedb.connect(str(data_dir / "lancedb"))
    if not _table_exists(db, TABLE_NAME):
        return
    table = db.open_table(TABLE_NAME)
    table.delete(f"path = '{_escape_sql(str(file_path))}'")
    _rebuild_bm25(table, data_dir)
