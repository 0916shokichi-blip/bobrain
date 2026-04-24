"""Hybrid search: BM25 + vector, combined via Reciprocal Rank Fusion."""
from __future__ import annotations

import pickle
from pathlib import Path

import lancedb
from fastembed import TextEmbedding
from rank_bm25 import BM25Okapi

from .indexer import MODEL_NAME, TABLE_NAME, tokenize


def rrf(rank_lists: list[list[str]], k: int = 60) -> dict[str, float]:
    scores: dict[str, float] = {}
    for rank_list in rank_lists:
        for rank, doc_id in enumerate(rank_list):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank + 1)
    return scores


def search(
    query: str,
    data_dir: Path,
    top_k: int = 5,
    namespaces: list[str] | None = None,
) -> list[dict]:
    model = TextEmbedding(model_name=MODEL_NAME)
    q_vec = [float(x) for x in next(iter(model.query_embed([query])))]

    db = lancedb.connect(str(data_dir / "lancedb"))
    table = db.open_table(TABLE_NAME)
    vector_results = table.search(q_vec).limit(top_k * 3).to_list()
    if namespaces:
        vector_results = [r for r in vector_results if r["namespace"] in namespaces]
    vector_ranked_ids = [r["id"] for r in vector_results]

    with (data_dir / "bm25.pkl").open("rb") as f:
        bm25_data = pickle.load(f)
    bm25: BM25Okapi = bm25_data["bm25"]
    q_tokens = tokenize(query)
    bm25_scores = bm25.get_scores(q_tokens)
    bm25_order = sorted(range(len(bm25_scores)), key=lambda i: -bm25_scores[i])
    bm25_ranked_ids: list[str] = []
    for idx in bm25_order[: top_k * 3]:
        if namespaces and bm25_data["namespaces"][idx] not in namespaces:
            continue
        bm25_ranked_ids.append(bm25_data["ids"][idx])

    fused = rrf([vector_ranked_ids, bm25_ranked_ids])
    top_ids = sorted(fused.keys(), key=lambda i: -fused[i])[:top_k]

    meta: dict[str, dict] = {r["id"]: r for r in vector_results}
    for idx, doc_id in enumerate(bm25_data["ids"]):
        if doc_id in top_ids and doc_id not in meta:
            meta[doc_id] = {
                "id": doc_id,
                "text": bm25_data["texts"][idx],
                "path": bm25_data["paths"][idx],
                "namespace": bm25_data["namespaces"][idx],
            }

    return [
        {
            "id": i,
            "path": meta[i]["path"],
            "namespace": meta[i]["namespace"],
            "text": meta[i]["text"][:500],
            "score": fused[i],
        }
        for i in top_ids
        if i in meta
    ]
