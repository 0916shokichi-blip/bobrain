"""Indexer: markdown → chunks → embeddings → LanceDB + BM25 JSON state."""
from __future__ import annotations

import hashlib
import os
import re
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import lancedb
import pathspec
from fastembed import TextEmbedding
from fugashi import Tagger
from rank_bm25 import BM25Okapi
from tqdm import tqdm

from .bm25_state import LEGACY_PICKLE_FILE, save_state

MODEL_NAME = "intfloat/multilingual-e5-large"
VECTOR_DIM = 1024
TABLE_NAME = "chunks"


def fastembed_cache_dir(data_dir: Path | None = None) -> str:
    """Persistent fastembed cache dir.

    fastembed の default cache は ``tempfile.gettempdir()`` ベースで、macOS では
    ``/var/folders/.../T/fastembed_cache`` に landing する。これは再起動で揮発する
    領域なので、~2GB の e5-large weights が毎回消える。``data_dir`` 配下に明示する
    ことで永続化する (既定 ``~/.bobrain/fastembed_cache``)。
    """
    if data_dir is None:
        data_dir = Path(
            os.environ.get("BOBRAIN_DATA", str(Path.home() / ".bobrain"))
        ).expanduser()
    cache_dir = data_dir / "fastembed_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return str(cache_dir)

# Directories we never want to scan, even when the user points --root at a
# parent that contains them. Without this, `bobrain index ~/myrepo` happily
# walks into .venv/ (hundreds of vendored READMEs) or node_modules/.
_EXCLUDE_DIRS = frozenset({
    ".venv", "venv", ".env",
    "node_modules",
    ".git",
    "__pycache__",
    ".mypy_cache", ".ruff_cache", ".pytest_cache",
    "dist", "build", ".cache",
    ".obsidian", ".trash",
})

IGNORE_FILENAME = ".bobrainignore"

# Namespaces flow into LanceDB SQL filter strings (`namespace = '...'`).
# We restrict them to alphanumeric + ``_-`` and a sane length so the only
# escape concern downstream is the single quote, which `_escape_sql`
# still handles. CLI/build_index validates before the value reaches SQL.
_NAMESPACE_RE = re.compile(r"^[A-Za-z0-9_\-]{1,64}$")


def validate_namespace(namespace: str) -> str:
    """Reject namespaces that aren't safe to interpolate into SQL.

    Returns the namespace unchanged on success; raises ValueError otherwise.
    """
    if not _NAMESPACE_RE.match(namespace):
        raise ValueError(
            f"namespace must match {_NAMESPACE_RE.pattern!s} (got: {namespace!r})"
        )
    return namespace


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


def _load_ignore_specs(
    root: Path, excludes: set[str]
) -> list[tuple[Path, pathspec.PathSpec]]:
    """Find every `.bobrainignore` under root and return (anchor_dir, spec) pairs.

    Each spec's anchor_dir is the directory containing the ignore file; patterns
    are evaluated relative to it (gitignore semantics). Files inside hard-coded
    excluded directories (`.venv`, `.git`, ...) are never read.
    """
    specs: list[tuple[Path, pathspec.PathSpec]] = []
    for ignore_file in root.rglob(IGNORE_FILENAME):
        if not ignore_file.is_file():
            continue
        if any(part in excludes for part in ignore_file.parts):
            continue
        try:
            lines = ignore_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        spec = pathspec.PathSpec.from_lines("gitignore", lines)
        specs.append((ignore_file.parent, spec))
    return specs


def _is_path_ignored(
    path: Path, specs: list[tuple[Path, pathspec.PathSpec]]
) -> bool:
    for anchor, spec in specs:
        try:
            rel = path.relative_to(anchor)
        except ValueError:
            continue
        if spec.match_file(rel.as_posix()):
            return True
    return False


def iter_markdown(
    root: Path, extra_excludes: Iterable[str] = ()
) -> Iterable[Path]:
    excludes = _EXCLUDE_DIRS | set(extra_excludes)
    specs = _load_ignore_specs(root, excludes)
    for p in root.rglob("*.md"):
        if not p.is_file():
            continue
        if any(part in excludes for part in p.parts):
            continue
        if specs and _is_path_ignored(p, specs):
            continue
        yield p


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


def build_chunks(
    roots: Path | Iterable[Path],
    namespace: str,
    extra_excludes: Iterable[str] = (),
) -> list[Chunk]:
    roots_list = [roots] if isinstance(roots, Path) else list(roots)
    chunks: list[Chunk] = []
    seen: set[Path] = set()
    for root in roots_list:
        for p in iter_markdown(root, extra_excludes):
            resolved = p.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            chunks.extend(chunks_for_file(p, namespace))
    return chunks


def chunks_for_file(file_path: Path, namespace: str) -> list[Chunk]:
    # Strict UTF-8: silently dropping garbage with errors="ignore" used to
    # leak binary fragments (and the ChatML / zero-width markers they may
    # contain) into the index. A skip-with-warning is louder but safer.
    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"[indexer] skipping {file_path}: not valid UTF-8", file=sys.stderr)
        return []
    return [
        Chunk(
            id=hash_id(str(file_path), i, c),
            text=c,
            path=str(file_path),
            namespace=namespace,
        )
        for i, c in enumerate(chunk_markdown(text))
    ]


def embed_texts(texts: list[str], data_dir: Path | None = None) -> list[list[float]]:
    """Embed documents for indexing. Uses passage_embed so e5 prefixes are applied."""
    model = TextEmbedding(model_name=MODEL_NAME, cache_dir=fastembed_cache_dir(data_dir))
    out: list[list[float]] = []
    bar = tqdm(
        total=len(texts),
        desc="embed",
        unit="ch",
        disable=_progress_disabled(),
        file=sys.stderr,
        leave=False,
    )
    for v in model.passage_embed(texts):
        out.append([float(x) for x in v])
        bar.update(1)
    bar.close()
    return out


def _progress_disabled() -> bool:
    """Suppress progress bars when not running in a TTY or when explicitly silenced."""
    if os.environ.get("BOBRAIN_QUIET"):
        return True
    return not sys.stderr.isatty()


@contextmanager
def _phase(name: str, n: int | None = None):
    """Time a phase and print 'phase: 1.2s (N items)' to stderr on exit."""
    t0 = time.perf_counter()
    try:
        yield
    finally:
        dt = time.perf_counter() - t0
        suffix = f" ({n} items)" if n is not None else ""
        print(f"  {name}: {dt:.1f}s{suffix}", file=sys.stderr)


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


def _chunks_to_rows(chunks: list[Chunk], data_dir: Path | None = None) -> list[dict]:
    if not chunks:
        return []
    texts = [c.text for c in chunks]
    vectors = embed_texts(texts, data_dir=data_dir)
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
    """Re-dump BM25 state as JSON from every row currently in the LanceDB
    table. Drops any legacy pickle file once the new state is written so
    the next ``load_state`` call doesn't need the deprecation fallback.
    """
    arrow_table = table.to_arrow().select(["id", "text", "path", "namespace"])
    records = arrow_table.to_pylist()
    texts = [r["text"] for r in records]
    tokenized = [tokenize(t) for t in texts]
    bm25 = BM25Okapi(tokenized) if tokenized else None
    save_state(
        {
            "bm25": bm25,
            "ids": [r["id"] for r in records],
            "texts": texts,
            "paths": [r["path"] for r in records],
            "namespaces": [r["namespace"] for r in records],
        },
        data_dir,
    )
    legacy = data_dir / LEGACY_PICKLE_FILE
    if legacy.exists():
        legacy.unlink()


def _table_exists(db, name: str) -> bool:
    # LanceDB >= 0.30 returns a ListTablesResponse(tables=[...]) wrapper,
    # so `name in db.list_tables()` is always False. Use `.tables`.
    return name in db.list_tables().tables


def _table_vector_dim(table) -> int | None:
    """Return the declared vector dim of the chunks table, or None if unknown."""
    for field in table.schema:
        if field.name == "vector" and hasattr(field.type, "list_size"):
            return field.type.list_size
    return None


def _upsert_rows(data_dir: Path, where: str, rows: list[dict]):
    """Delete existing rows matching `where`, then insert `rows`. Returns the table."""
    data_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(data_dir / "lancedb"))

    if _table_exists(db, TABLE_NAME):
        table = db.open_table(TABLE_NAME)
        existing_dim = _table_vector_dim(table)
        if existing_dim is not None and existing_dim != VECTOR_DIM:
            # The embedding model changed since this index was built; the old
            # FixedSizeList column can't accept new rows. Drop and let the
            # rest of this call recreate the table with the current schema.
            db.drop_table(TABLE_NAME)
        else:
            table.delete(where)
            if rows:
                table.add(rows)
            return table

    if rows:
        return db.create_table(TABLE_NAME, data=rows)
    return None


def _escape_sql(value: str) -> str:
    # Order matters: escape backslashes first so we don't double-escape
    # the ones we just introduced for single quotes. LanceDB / DataFusion
    # currently treats backslash literally, but hardening here keeps the
    # call site safe against future engine swaps.
    return value.replace("\\", "\\\\").replace("'", "''")


def _existing_chunk_ids_for_namespace(
    data_dir: Path, namespace: str
) -> set[str]:
    """Return the chunk IDs currently stored for `namespace`.

    Returns an empty set when the DB doesn't exist yet, when the table is
    missing, or when the stored vector dim doesn't match the current model
    (in which case the caller should fall through to a full rebuild via
    :func:`_diff_upsert`, which drops the table).
    """
    db_path = data_dir / "lancedb"
    if not db_path.exists():
        return set()
    db = lancedb.connect(str(db_path))
    if not _table_exists(db, TABLE_NAME):
        return set()
    table = db.open_table(TABLE_NAME)
    existing_dim = _table_vector_dim(table)
    if existing_dim is not None and existing_dim != VECTOR_DIM:
        return set()
    # Pull just (id, namespace); skipping the vector column keeps this cheap
    # even for namespaces with thousands of chunks. Filtering in Python is
    # fine at the realistic scale (<100k rows per Vault).
    records = table.to_arrow().select(["id", "namespace"]).to_pylist()
    return {r["id"] for r in records if r["namespace"] == namespace}


def _diff_upsert(
    data_dir: Path,
    namespace: str,
    ids_to_delete: set[str],
    rows_to_add: list[dict],
):
    """Apply a namespace-scoped diff to the chunks table.

    Deletes the given IDs (within `namespace`) and inserts new rows.
    If the existing vector dim doesn't match, drops the whole table and
    rebuilds from `rows_to_add` (matches `_upsert_rows` migration behavior).
    """
    data_dir.mkdir(parents=True, exist_ok=True)
    db = lancedb.connect(str(data_dir / "lancedb"))

    if _table_exists(db, TABLE_NAME):
        table = db.open_table(TABLE_NAME)
        existing_dim = _table_vector_dim(table)
        if existing_dim is not None and existing_dim != VECTOR_DIM:
            db.drop_table(TABLE_NAME)
        else:
            ns_escaped = _escape_sql(namespace)
            if ids_to_delete:
                ids_list = list(ids_to_delete)
                # Batch large IN clauses; DataFusion handles them, but
                # 10k-id strings are noisier than necessary.
                for i in range(0, len(ids_list), 1000):
                    batch = ids_list[i : i + 1000]
                    ids_csv = ", ".join(
                        f"'{_escape_sql(id_)}'" for id_ in batch
                    )
                    table.delete(
                        f"namespace = '{ns_escaped}' AND id IN ({ids_csv})"
                    )
            if rows_to_add:
                table.add(rows_to_add)
            return table

    if rows_to_add:
        return db.create_table(TABLE_NAME, data=rows_to_add)
    return None


def build_index(
    roots: Path | Iterable[Path],
    namespace: str,
    data_dir: Path,
    extra_excludes: Iterable[str] = (),
    full_rebuild: bool = False,
) -> int:
    """Re-index all markdown under `roots` for `namespace` (other namespaces untouched).

    Hash-aware diff: only chunks whose ``(path, idx, text)`` hash isn't
    already in the index get embedded. Removed chunks (existing IDs that
    are absent from the new scan) are deleted. Unchanged chunks are
    skipped entirely — no embedding, no rewrite. For a Vault with 642
    chunks where 20 changed since last index, expect ~3% of the previous
    embed cost.

    Pass ``full_rebuild=True`` to force re-embedding every chunk and
    rewrite BM25 state from scratch. Useful when the BM25 sidecar is
    suspected to be out of sync or the table needs to be repacked.

    Returns the total chunk count in the namespace after this run (matches
    pre-diff behavior so callers / tests don't have to change).
    """
    validate_namespace(namespace)
    with _phase("scan"):
        new_chunks = build_chunks(roots, namespace, extra_excludes)

    new_by_id: dict[str, Chunk] = {}
    for c in new_chunks:
        # In the rare case two scanned chunks collide on hash_id (same
        # path+idx+text), keep the first; embedding the same row twice is
        # wasted work.
        new_by_id.setdefault(c.id, c)
    new_ids = set(new_by_id)
    if full_rebuild:
        # Treat the namespace as if no prior index existed: every chunk
        # gets re-embedded and every existing row gets replaced.
        existing_ids: set[str] = set()
    else:
        existing_ids = _existing_chunk_ids_for_namespace(data_dir, namespace)

    to_add_ids = new_ids - existing_ids
    to_add = [new_by_id[i] for i in to_add_ids]
    ids_to_delete = existing_ids - new_ids
    kept = len(existing_ids & new_ids)

    if not _progress_disabled():
        mode = "full-rebuild" if full_rebuild else "diff"
        print(
            f"  {mode}: +{len(to_add)} new / -{len(ids_to_delete)} removed / "
            f"={kept} unchanged",
            file=sys.stderr,
            flush=True,
        )

    with _phase("embed", n=len(to_add)):
        rows = _chunks_to_rows(to_add, data_dir=data_dir)

    # Skip the DB / BM25 write entirely if nothing changed. The on-disk
    # state is already correct in that case and rewriting BM25 just to
    # produce identical bytes is wasted I/O. full_rebuild bypasses this
    # shortcut by replacing the entire namespace via _upsert_rows.
    if full_rebuild:
        with _phase("db-write", n=len(rows)):
            table = _upsert_rows(
                data_dir,
                where=f"namespace = '{_escape_sql(namespace)}'",
                rows=rows,
            )
    else:
        if not rows and not ids_to_delete:
            return len(new_chunks)
        with _phase("db-write", n=len(rows) + len(ids_to_delete)):
            table = _diff_upsert(data_dir, namespace, ids_to_delete, rows)
    if table is None:
        return 0
    with _phase("bm25"):
        _rebuild_bm25(table, data_dir)
    return len(new_chunks)


def reindex_file(file_path: Path, namespace: str, data_dir: Path) -> int:
    """Re-index a single file. Existing rows for that path (any namespace) are replaced."""
    chunks = chunks_for_file(file_path, namespace)
    rows = _chunks_to_rows(chunks, data_dir=data_dir)
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
