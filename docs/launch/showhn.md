# Show HN draft (v1)

起草日: 2026-04-28
投稿想定: 5/5 火曜 米東部 6:30-7:30 AM = 日本時間 火曜 19:30-20:30
推敲ステータス: marketer-ja v1 (Gamma v0 全却下を受けて再起草)、再 Gamma 待ち

## title

```
Show HN: Bobrain – A local-first hybrid RAG MCP server for notes and code
```

## body

```markdown
A few weeks ago, I was deep in an MCP chunking problem and asked Claude to
search across my Obsidian vault and a couple of side-project repos. It
surfaced a note from late 2022 — written by me, on the same chunking
question, with a working answer I'd already arrived at. I had no memory of
writing it. The note was titled something I would never search for now.

Bobrain came out of that. It's an MCP server that indexes Markdown notes
and Git repositories into one hybrid retrieval backend, and exposes it to
Claude / Claude Desktop / Cursor. Notes and code share a single ranked
list, but live in separate namespaces so you can scope queries.

The retrieval stack: BM25 with `fugashi` + `unidic-lite` for Japanese
morphology (I write JP/EN mixed), dense embeddings from
`multilingual-e5-large` on ONNX via fastembed, RRF fusion. Pure dense
missed obvious exact-term recall on technical notes; the fusion did not.

One thing the namespace separation gave me that I didn't expect: when I
query notes-only, the retrieval surfaces older notes more often than I'd
intuit. Recency bias in my own attention is stronger than I realized — the
ranking does not share it.

Status: 0.1.0, Markdown-only today. PDF and AST-aware code chunking are
roadmap, not shipped. MIT licensed.

Install: `pipx install bobrain` or `uvx bobrain`
Repo: https://github.com/0916shokichi-blip/bobrain

The choice I'm least sure about is `multilingual-e5-large` over `bge-m3` —
my pick was qualitative across ~30 queries on a JP/EN corpus. If anyone
has rigorous comparison data on mixed-language technical notes, I'd take a
different default.
```

## v0 → v1 で何を変えたか

- **タイトル**: "and PDFs" 削除（未対応の自白回避）。"multi-source" の中央値構文も削除し、簡素化
- **冒頭**: 「ripgrep と Obsidian 切替が面倒」という道具選択ピッチを廃止し、「2022 年の自分のメモが今の質問に既に答えていた / 書いたことを覚えていない」という具体的アネクドートに置換。日付感あり、事象開示のみで vision 示唆
- **bullet 廃止**: 3 つの spec dump を散文 1 段落に圧縮 + 「namespace 分離が引き起こした体験の質」を 1 段落追加（「自分の注意の recency bias より検索のほうが古い記憶に公平」= 体験の発見であって spec ではない）
- **closing 変更**: "Happy to talk about... or anything else" 死語削除。技術質問 1 つ（e5-large vs bge-m3 の rigorous data）に絞った
- **戦争比喩排除**: "lost the same battle" を完全削除

## 投稿先別の注意点（v0 から継続）

- **投稿時刻**: 米東部火曜 6:30-7:30 AM（日本時間 火曜 19:30-20:30）
- **タイトル**: HN ガイドラインで `Show HN:` プレフィクス必須、`–` (en-dash) 慣例
- **self-promotion**: 本文に "powerful" "revolutionary" 等が混ざっていないか最終確認 → クリア
- **初動で答えるべき暗黙の質問**: (1) なぜ MCP？CLI じゃダメか (2) なぜ既存 RAG ライブラリじゃないのか (3) どこが Knowledge-RAG / LlamaIndex と違うのか

## 想定 Q&A（初動 90 分用）

1. **Q**: How is this different from Knowledge-RAG / LlamaIndex / Cognee?
   **A**: Knowledge-RAG is the closest neighbor — single-vault Obsidian focus. Bobrain's bet is multi-source from day one (notes + code repos, namespace-separated). LlamaIndex is a framework, not a server; you'd have to build the MCP layer yourself. Cognee leans toward larger, cloud-friendly graph deployments. Bobrain optimizes for "one solo developer's brain across notes and side projects, fully local."

2. **Q**: Why MCP and not just a CLI tool?
   **A**: I use Claude Desktop and Cursor for most actual work. A CLI means context-switching out of the editor; MCP means the assistant can pull relevant chunks during a conversation without me leaving. The CLI version exists too (`bobrain query`), but MCP is where it earns its keep.

3. **Q**: Why BM25 + dense instead of just dense embeddings?
   **A**: For my own technical notes, exact-term recall mattered more than I expected — function names, library names, JP technical terms. Pure dense missed obvious matches. BM25 (with `fugashi` for Japanese tokenization) catches what dense softens. RRF fusion was the simplest reliable combiner I could test.

4. **Q**: How does it compare to Claude-Context (Zilliz)?
   **A**: Claude-Context is code-focused and integrates with Zilliz Cloud. Bobrain is local-only and treats notes as first-class alongside code. Different bet on what a developer's "knowledge surface" looks like.

5. **Q**: Roadmap?
   **A**: PDF ingestion next (papers, design docs), then code-AST-aware chunking so function/class boundaries aren't shredded mid-block. Pro version with sync/multi-machine is being explored but the OSS core stays MIT.
