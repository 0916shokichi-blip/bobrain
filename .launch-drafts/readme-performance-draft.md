# README "How it performs" セクション draft

DR 提案 D-7（コンテキスト節約量の実数提示）を bobrain 文脈で受けるための **README 中盤追加セクション** の draft。**hero copy には触らない**（L0 anti_patterns 機能羅列違反回避）。

## 配置位置

`README.md` の `## Roadmap`（L108）直前に挿入。`## MCP client setup`（L76）の後。

## 採用前提

- `/playable-gate bobrain --target docs/readme-performance-section.md` で 4 段関門通過が **必須**
- Gamma 平凡化攻撃で「数値が機能羅列に滑っていないか」を確認
- L0 anti_patterns カテゴリ 4（機能ベース差別化）に逆戻りしていないか主確認

## draft 本文（v0、要 playable-gate）

```markdown
## How it performs

Real numbers from my own dogfooding setup (4 namespaces, 1042 chunks total):

| Phase | Measured |
|---|---|
| Index size | 1042 chunks across 4 namespaces (notes / code / two LLM wikis) |
| Embedding (CPU, single thread) | 1.4 – 2.4 sec/chunk on `multilingual-e5-large` ONNX |
| Cold start | 15 – 30 sec for first-time ONNX weight download (~2.2 GB) |
| Subsequent runs | weights are cached locally; no further download |
| Hybrid retrieval | BM25 + dense, fused via Reciprocal Rank Fusion |

> These numbers are from my single laptop, not a benchmark suite. Your milage will vary by chunk size, language mix, and CPU. The point is that everything runs locally with **zero cloud calls per query**.

### Context cost compared to full-context loading

When an agent needs to answer "where did I write about X" against a 1000+ note vault, two paths are common:

1. Stream the whole vault into the model context — fast to set up, but burns tokens proportional to vault size on every turn.
2. Use `bobrain search_docs` — only the top-k relevant chunks (default k=5) are returned, typically a few KB regardless of vault size.

For reference, the four namespaces above total roughly **<TBD: measured byte count> KB** of source markdown, while a typical k=5 search returns **<TBD: measured byte count> KB** of chunks. The retrieval delta is what bobrain trades for an upfront one-time embedding cost.

> The TBD numbers will be measured before launch via `bobrain search "<query>" -k 5 --json` against representative queries. See `docs/research/showhn-strategy-2026-04-29.md` for why these specific numbers matter on Show HN.
```

## 実測タスク（playable-gate 通す前にやる）

1. 代表クエリ 3 件決定（例: "MCP chunking", "決済 MoR 比較", "ドメイン取得方針"）
2. 各クエリで `bobrain search -k 5 --json` のレスポンス byte 数を計測
3. 各 namespace の Markdown 合計 byte を `find ... -name '*.md' | xargs wc -c` で計測
4. 表に埋めて draft を確定 → playable-gate に投げる

実装は別セッション or ユーザー指示後に。本 draft は構造提示のみ。

## L0 anti_patterns 自己チェック

- ❌ 「世界最速」「究極の」型ワード未使用 ✓
- ❌ 機能羅列のみ（hero に出していない）→ ✓ hero は体験文を維持、本セクションは中盤の補足
- ❌ 競合直接攻撃（vs ChromaDB 等を本文に書かない）→ ✓ 比較は「2 つの一般的な path」で抽象化
- ✓ 自分の実測データのみ提示（誇大表現なし）
- ✓ "Your milage will vary" で謙虚さ担保

## 関連参照

- DR 整形版: `docs/research/showhn-strategy-2026-04-29.md` § 7 適用判断
- Memory: `showhn_launch_benchmarks_2026.md` 「2026 評価軸シフト」
- L0 director: `.agents/director/anti_patterns.md`
