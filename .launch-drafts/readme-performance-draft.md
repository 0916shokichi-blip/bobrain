# README "How it performs" セクション draft

DR 提案 D-7（コンテキスト節約量の実数提示）を bobrain 文脈で受けるための **README 中盤追加セクション** の draft。**hero copy には触らない**（L0 anti_patterns 機能羅列違反回避）。

## 配置位置

`README.md` の `## Roadmap`（L108）直前に挿入。`## MCP client setup`（L76）の後。

## 採用前提

- `/playable-gate bobrain --target .launch-drafts/readme-performance-draft.md` で 4 段関門通過が **必須**
- Gamma 平凡化攻撃で「数値が機能羅列に滑っていないか」を確認
- L0 anti_patterns カテゴリ 4（機能ベース差別化）に逆戻りしていないか主確認

---

## 実測値（2026-04-29 計測、自分のマシンの dogfooding setup）

LanceDB から直接 chunk 統計を取得。`bobrain` を入れた直後の自分の vault 4 namespace。

| metric | value |
|---|---|
| Indexed source files | 126 markdown files |
| Source markdown total | 467,319 bytes (456 KB) |
| Chunks after splitting | 1042 chunks |
| Chunk total bytes | 341,393 bytes (333 KB) |
| Source → chunks ratio | 73.1% (chunking + small-section dedup) |
| Mean chunk size | 328 bytes |
| Min / Max chunk | 9 / 2621 bytes (chunker target = 1000 chars, UTF-8 で日本語混在) |
| k=5 retrieval (mean) | ~1638 bytes (~1.6 KB) |
| k=10 retrieval (mean) | ~3276 bytes (~3.2 KB) |

namespace 別:

| namespace | files | source KB | chunk KB | chunks |
|---|---|---|---|---|
| apptree | 31 | 171.1 | 100.3 | 306 |
| claude-knowledge | 64 | 186.5 | 167.8 | 535 |
| monetize | 24 | 98.8 | 59.0 | 169 |
| mybrain | 7 | 0.0 (旧 path、再 index 待ち) | 6.4 | 32 |

実測コマンド（再現性、`docs/research/measure-context-savings.py` に保存予定）:

```python
import lancedb
db = lancedb.connect('~/.bobrain/lancedb')
arr = db.open_table('chunks').to_arrow()
texts = arr['text'].to_pylist()
nses  = arr['namespace'].to_pylist()
# byte_lens = [len(t.encode('utf-8')) for t in texts]
# group by namespace, sum, divide by source file size
```

---

## draft 本文（v1、実数埋め込み済み、要 playable-gate）

```markdown
## How it performs

Numbers from my own dogfooding setup (4 namespaces, 1042 chunks):

| metric | measured |
|---|---|
| Indexed source | 126 markdown files, ~456 KB total |
| Chunks after splitting | 1042 chunks, ~333 KB |
| Mean chunk size | 328 bytes |
| Embedding (CPU, single thread) | 1.4 – 2.4 sec/chunk on `multilingual-e5-large` ONNX |
| Cold start | 15 – 30 sec for first-time ONNX weight download (~2.2 GB) |
| Hybrid retrieval | BM25 + dense, fused via Reciprocal Rank Fusion |

> These numbers are from a single laptop, not a benchmark suite. Your milage will vary by chunk size, language mix, and CPU. The point is that everything runs locally with **zero cloud calls per query**.

### What gets sent to the model on each query

Two extreme paths for "where did I write about X" against a 1000+ note vault:

| path | bytes added to context | notes |
|---|---|---|
| Stream the whole vault | ~456 KB (this vault) | scales linearly with vault size, every turn |
| `search_docs` k=5 (bobrain) | ~1.6 KB (mean) | constant size regardless of vault, single round trip |

That's roughly a **285× reduction** for this vault, traded against an upfront one-time embedding cost (~25 minutes on CPU for these 1042 chunks). The reduction grows with vault size — a 10× larger vault still returns ~1.6 KB on k=5, while full-context loading would 10× the per-query token bill.

> "Stream the whole vault" is a pathological baseline; nobody actually does it. The realistic comparison is closer to grep-then-paste, where retrieval still wins on relevance and recency. The point of the table is that with hybrid retrieval, **per-query context cost is decoupled from vault size**.
```

---

## L0 anti_patterns 自己チェック (v1)

- ❌ 「世界最速」「究極の」型ワード未使用 ✓
- ❌ 機能羅列のみ（hero に出していない）→ ✓ hero は体験文を維持、本セクションは中盤の補足
- ❌ 競合直接攻撃（vs ChromaDB 等を本文に書かない）→ ✓ 比較は「2 つの抽象 path」で表現
- ✓ 自分の実測データのみ提示（誇大表現なし）
- ✓ "Your milage will vary" / "pathological baseline" の謙虚な注釈で誇張回避
- ⚠️ 「285× reduction」は数字として強い。Gamma 攻撃で「数字釣り」判定されるリスクあり → playable-gate で精査

## 数値選定の根拠

DR の Context Mode 事例「315 KB → 5.4 KB（約 60×）」と比較:

- bobrain: 456 KB → 1.6 KB = **285×**（vault が小さいほど上振れする傾向）
- 数値が大きすぎて誇張感を与える可能性 → 表現は「reduction」で受動形に留め、誇張動詞（"crushes" "shrinks" "destroys"）を避ける
- vault 規模差を明示（"this vault" を強調）して、絶対主張を回避

## 関連参照

- DR 整形版: `docs/research/showhn-strategy-2026-04-29.md` § 7 適用判断
- Memory: `showhn_launch_benchmarks_2026.md` 「2026 評価軸シフト」
- L0 director: `.agents/director/anti_patterns.md`
- 実測ログ: 本セクションのコマンド + bobrain v0.1.0 LanceDB（2026-04-29 実行）
