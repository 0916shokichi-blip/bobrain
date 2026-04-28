# r/LocalLLaMA draft (v0)

起草日: 2026-04-28
投稿想定: 5/5 火曜 米東部 9-11 AM = 日本時間 火曜 22-24 時（Show HN と同日夜の 2 投稿目）
推敲ステータス: marketer-ja 起草版、未 playable-gate / 未 humanizer-ja

## title

```
[Project] Bobrain — fully local hybrid RAG MCP server (BM25 + multilingual-e5-large via ONNX), built for searching across notes and code
```

## body

```markdown
Sharing a side project I've been running for a few weeks and finally
released as 0.1.0 on PyPI yesterday. Posting here because LocalLLaMA folks
tend to care about the implementation choices, not just the pitch.

**What it is**: an MCP server that indexes Markdown notes (Obsidian vaults
or any folder) and Git repositories into a single hybrid retrieval
backend, exposed to Claude / Claude Desktop / Cursor via MCP. Fully local,
no API calls, ONNX runtime.

**Why I'm posting it here specifically**: the retrieval stack has a few
choices I'd like feedback on, especially from people running their own
embedding pipelines.

**Stack**:
- BM25 with `fugashi` + `unidic-lite` for Japanese morphological analysis
  (I write in mixed JP/EN, and standard whitespace tokenization is useless
  for Japanese).
- Dense: `intfloat/multilingual-e5-large` via fastembed's ONNX backend.
  Picked over `bge-m3` after testing — e5-large was meaningfully better
  on my JP technical notes corpus, though I don't have rigorous
  benchmarks to share, just qualitative.
- Reciprocal Rank Fusion (k=60) for combining the two. Tried weighted
  linear combination first; RRF was less fiddly and equally good on my
  test queries.
- Namespace separation between sources, so you can query notes-only,
  code-only, or both. Mixing notes and code is good for "where did I
  write about X" but bad for "find the function that does Y."

**Numbers**: 1,042 chunks indexed from my current vault. Indexing runs
~1.4–2.4 sec/chunk on M-series Mac (chunk size variation). Query latency
is sub-second on this index size, but I haven't stressed it past 10K
chunks yet — would love to hear from anyone who tries with a larger
vault.

**Status disclaimer**: early prototype. Markdown-only today. PDF and
code-AST-aware chunking are on the roadmap but not shipped. MIT licensed.

Install: `pipx install bobrain` or `uvx bobrain`
Repo: https://github.com/0916shokichi-blip/bobrain

Genuinely curious if anyone has tried `multilingual-e5-large` vs `bge-m3`
on mixed-language corpora and has data — my pick was based on a few
dozen test queries, not anything you'd call rigorous.

(Mods: happy to remove if this falls outside self-promotion guidance.)
```

## 投稿先別の注意点

- **投稿時刻**: r/LocalLLaMA は 24 時間活発だが、米国 EST 火曜 9-11 AM（日本時間 火曜 22-24 時）が技術系の長文に伸びやすい。月曜は週末スレが残っていて埋もれる
- **self-promotion rule**: r/LocalLLaMA は 9:1 ルール（自分の投稿は 10% まで）が緩めだが、mod 判断で削除されることがある。**最終行の "(Mods: happy to remove if this falls outside self-promotion guidance.)"** は draft 段階で残し、投稿前に mod に DM で確認するのが安全
- **deep に読まれるための工夫**: 「e5-large vs bge-m3 のデータが欲しい」という具体的な質問を最後に置き、コメント参加のフックにした。技術コミュニティは「こいつは本気で困っている / 知りたがっている」が伝わると伸びる
- **初動で答えるべき暗黙の質問**: (1) なぜ ChromaDB / Qdrant / Weaviate を使わなかったのか (2) ONNX vs llama.cpp embedding (3) なぜ MCP

## 想定 Q&A（初動 90 分用）

1. **Q**: Why not use ChromaDB / Qdrant / Weaviate as the backend?
   **A**: For 1K-100K chunks on a single user's machine, the operational overhead of running a separate vector DB outweighs the benefits. Bobrain stores vectors in SQLite + flat files. If someone needed to scale past 1M chunks I'd reconsider, but the target user is one developer's knowledge surface, not a team's.

2. **Q**: Have you tried `bge-m3` head-to-head with `e5-large`? Any benchmark numbers?
   **A**: Honestly no rigorous numbers — I ran ~30 queries from my actual usage pattern and e5-large felt better on JP/EN mixed technical content. bge-m3 is competitive and the multi-vector mode is interesting; if anyone has solid eval data I'd genuinely take a different default. This is the choice I'm least confident in.

3. **Q**: Why MCP instead of just an HTTP API or CLI?
   **A**: Both exist (`bobrain query` CLI works), but MCP integration is what makes it useful day-to-day for me — Claude Desktop / Cursor pull chunks mid-conversation without me leaving the editor. MCP is a thin protocol layer; the retrieval engine is the real work.

4. **Q**: How does the Japanese tokenization affect English-only users?
   **A**: BM25 detects script and dispatches per-document. English-only vaults get standard tokenization with no `fugashi` overhead. The cost is a slightly heavier install (`unidic-lite` is ~50MB) — I'm considering making JP support an extras dependency.

5. **Q**: How does this compare to `llama.cpp` embedding + your own glue code?
   **A**: Mostly: I didn't want to maintain the glue. fastembed wraps ONNX + tokenizer + pooling in one package and the perf is fine for this scale. If someone has a better model that's only on llama.cpp I'd add an adapter, but starting with fastembed kept the surface area small.

## 気をつけたこと（anti_patterns 回避メモ）

- **機能羅列を避けた箇所**: 機能リストではなく **「選択肢ごとの trade-off」** で書いた。"BM25 ... because Japanese needs morphology" / "RRF over weighted linear because less fiddly" / "namespace separation because mixing is good for X but bad for Y"
- **誇大表現を避けた箇所**: "fast" "powerful" "state-of-the-art" を一切使わず、"meaningfully better" "qualitative, not rigorous" "I'd love to hear" と **不確かさを残した**。LocalLLaMA は確信過剰を一番嫌うコミュニティ
- **体験文に寄せた箇所**: "I write in mixed JP/EN" "I don't have rigorous benchmarks to share, just qualitative" — 個人としての視点を残した
- **哲学を出さなかった箇所**: 完全に技術ドリブン。書き手の人格を一切出していない（LocalLLaMA はプロダクトくささを嫌うので、ここでは無人格が正解）

## 改稿で迷ったら削るポイント

- "(Mods: happy to remove if this falls outside self-promotion guidance.)" は自信があれば外す（弱腰に見えるリスク）
