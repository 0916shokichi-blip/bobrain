# r/LocalLLaMA draft (v1)

起草日: 2026-04-28
投稿想定: 5/5 火曜 米東部 9-11 AM = 日本時間 火曜 22-24 時
推敲ステータス: marketer-ja v1 (Gamma v0 全却下を受けて再起草)、再 Gamma 待ち

## title

```
[Project] Bobrain — fully local hybrid RAG MCP server (BM25 + multilingual-e5-large via ONNX), built for cross-corpus search over notes and code
```

## body

```markdown
0.1.0 on PyPI yesterday after a few weeks of dogfooding. Posting here
because the retrieval stack has a few choices I'd like pushback on.

Origin story, brief: I asked it about an MCP chunking question last month
and it pulled a note I wrote in 2022 with the answer already worked out. I
hadn't remembered writing it. That moment is what convinced me the
"single ranked list across notes + code" framing was worth shipping.

What it is: an MCP server that indexes Markdown notes (Obsidian vaults or
any folder) and Git repositories into one hybrid retrieval backend,
exposed to Claude / Claude Desktop / Cursor via MCP. Fully local, ONNX
runtime, no API calls.

Stack and the trade-offs I'm actually unsure about:

- **BM25 with `fugashi` + `unidic-lite`** for JP morphology. Standard
  whitespace tokenization is useless for Japanese, and I write JP/EN
  mixed. The cost is a ~50MB install bump from `unidic-lite` — I'm
  considering an extras dependency for non-JP users.
- **Dense: `multilingual-e5-large` via fastembed/ONNX over `bge-m3`**.
  Qualitative call on ~30 queries from my actual usage; not rigorous. The
  side-effect I noticed: pure dense softens function names and library
  names in technical notes. Hybrid catches them, single-stack didn't.
- **RRF (k=60) over weighted linear fusion**. Less fiddly, equally good
  on my queries.

Numbers: 1,042 chunks from my current vault, indexing ~1.4–2.4 sec/chunk
on M-series Mac, sub-second query at this scale. I haven't pushed past
10K chunks.

One thing I noticed dogfooding that wasn't in the design doc: namespace
separation between notes and code makes recency bias visible. Querying
notes-only surfaces older content more than I'd intuit on my own —
turns out my attention is more recency-biased than the index.

Markdown-only today. PDF and AST-aware code chunking on the roadmap.
MIT.

Install: `pipx install bobrain` or `uvx bobrain`
Repo: https://github.com/0916shokichi-blip/bobrain

The choice I'm least confident in: `e5-large` vs `bge-m3` on mixed JP/EN
technical corpora. If anyone has solid eval data, I'd genuinely change
the default.
```

## v0 → v1 で何を変えたか

- **冒頭刷新**: "Sharing a side project..." クリシェ廃止。"0.1.0 on PyPI yesterday" の事実から入り、続けて「2022 年の自分のメモがチャンキング問題の答えを既に持っていた / 覚えていない」アネクドートで事象開示。LocalLLaMA は確信過剰嫌いなので vision は匂わせる程度
- **bullet 構成変更**: 3 bullet 維持（LocalLLaMA は trade-off 構造好き）だが、各 bullet に「ユーザーが体験する違い」を混ぜた（特に dense bullet の「pure dense は function/library name を softening する」= retrieval stack 選択 → 体験差の橋渡し）
- **「namespace 分離が露見させた recency bias」段落追加**: spec ではなく dogfooding で気づいた事象、Show HN と同じ発見の質感を LocalLLaMA バージョンで（vision を匂わせるが、技術系の発見として書く）
- **"(Mods: happy to remove..." 削除**: 弱腰削除
- **closing は維持**: e5-large vs bge-m3 の rigorous data フックは v0 でも有効だったので残置

## 投稿先別の注意点（v0 から継続）

- **投稿時刻**: 米国 EST 火曜 9-11 AM（日本時間 火曜 22-24 時）
- **self-promotion rule**: 投稿前に mod に DM で確認するのが安全
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
