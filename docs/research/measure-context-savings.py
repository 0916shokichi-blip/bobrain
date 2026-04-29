"""Re-run this to refresh the numbers in the README "How it performs" section.

Reads chunks straight from LanceDB and computes:
- per-namespace source vs chunk byte counts
- mean chunk size and k=N retrieval byte estimates
- compression ratio source → chunks → k=5

Usage: `uv run python docs/research/measure-context-savings.py`
"""

from __future__ import annotations

import os
from collections import defaultdict
from pathlib import Path

import lancedb


def main(data_dir: Path | str = "~/.bobrain/lancedb") -> None:
    db = lancedb.connect(str(Path(data_dir).expanduser()))
    arr = db.open_table("chunks").to_arrow()
    texts = arr["text"].to_pylist()
    paths = arr["path"].to_pylist()
    nses = arr["namespace"].to_pylist()

    files: dict[str, set[str]] = defaultdict(set)
    chunk_bytes: dict[str, int] = defaultdict(int)
    for t, p, n in zip(texts, paths, nses, strict=True):
        files[n].add(p)
        chunk_bytes[n] += len(t.encode("utf-8"))

    print(f"total chunks: {len(texts)}")
    print()
    print(
        f'{"namespace":<20} {"files":>6} {"src_KB":>10} {"chunk_KB":>10} {"ratio":>7}'
    )
    total_src = 0
    for ns in sorted(files):
        src_b = 0
        miss = 0
        for f in files[ns]:
            try:
                src_b += os.path.getsize(f)
            except FileNotFoundError:
                miss += 1
        total_src += src_b
        cb = chunk_bytes[ns]
        ratio = cb / src_b if src_b else 0.0
        suffix = f" (missing {miss})" if miss else ""
        print(
            f"{ns:<20} {len(files[ns]):>6} {src_b/1024:>10.1f} "
            f"{cb/1024:>10.1f} {ratio:>6.1%}{suffix}"
        )

    total_chunk = sum(chunk_bytes.values())
    mean_chunk = total_chunk / len(texts)
    k5 = 5 * mean_chunk
    print()
    print(f"TOTAL src bytes:   {total_src:,} ({total_src/1024:.1f} KB)")
    print(f"TOTAL chunk bytes: {total_chunk:,} ({total_chunk/1024:.1f} KB)")
    print(f"src → chunks:      {total_chunk/total_src:.1%}")
    print(f"k=5 retrieval:     ~{k5:.0f} bytes (~{k5/1024:.1f} KB)")
    print(f"vs full src:       {total_src/k5:.0f}x reduction")


if __name__ == "__main__":
    main()
