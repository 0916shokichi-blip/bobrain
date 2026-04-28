# r/LocalLLaMA 派生 draft（v3 ベース、ローカル LLM 文化に合わせて調整）

**経緯**: Show HN v3 (`show-hn-final.md`) を r/LocalLLaMA 用に最小調整。
- ローカル LLM サブレディットの作法: 技術詳細厚め、cloud バッシング軽く、商用感薄く、self-promotion ルール準拠
- HN との差: HN は「I built X because Y」テンプレ許容、Reddit は「Hey r/X, built this thing」テンプレ許容
- 投稿時は flair `[Resources]` か `[Discussion]` を選ぶ（self-promotion flair があれば優先）

---

## タイトル候補

### 推奨: R-LLAMA-1
> Local MCP that indexes Obsidian + code repos in one hybrid search (BM25 + multilingual-e5, in-process)

- HN タイトルに比べて括弧内の技術詳細が深い → r/LocalLLaMA の作法
- 「multilingual-e5」を明示すると同 sub の embedding ヲタ層に刺さる
- 「in-process」で「Ollama も Docker も不要」を即明示

### 代替: R-LLAMA-2
> [Showcase] bobrain — Obsidian + code repos as separate namespaces, BM25 + e5 hybrid, runs in-process

- showcase flair 想定タイトル

---

## 本文

```
Hey r/LocalLLaMA — sharing a small thing I built because I kept running into a workflow gap.

My notes have been in an Obsidian vault for years (~/Documents/notes/), but every solved engineering problem is buried in the README of some old ~/code/<project>/. I'd hit "I know I wrote this somewhere" and have no good way to search across both with my AI client.

bobrain is a local MCP server that indexes both as separate namespaces and lets Claude / Cursor / Claude Desktop query across all of them at once.

**Stack**
- BM25 (rank-bm25) with MeCab Japanese tokenization out of the box
- multilingual-e5-large dense embeddings via fastembed (in-process ONNX, ~2.2GB cache after first run)
- LanceDB for vector + metadata storage
- Reciprocal rank fusion to combine the two retrievers
- watchdog for incremental reindex while you edit

Everything runs in-process. No Ollama daemon, no Docker, no cloud round-trips, no telemetry. Embeddings are CPU by default; CoreML / Metal acceleration is on the roadmap.

**What it does not do, by design**
- summarize chunks for you. What comes back is the chunk and the file path, nothing else (your LLM does the summarization if it wants to)
- send your notes anywhere
- require Obsidian to be running. Plain .md files on disk is enough

**Where it sits**
Existing Obsidian MCPs (engraph, obsidian-brain, vaultforge, mcpvault) all index a single vault. bobrain is the multi-root one — different design center.

**Install**
```
pipx install bobrain
bobrain index ~/Documents/notes -n notes
bobrain index ~/code/myproject -n code
bobrain serve  # Then point your MCP client at it
```

**Repo**: https://github.com/0916shokichi-blip/bobrain
**License**: MIT
**Status**: 0.1.0 on PyPI, early prototype

Solo project. Design and tests are mine; commits are not squashed if you want to read along. Claude Code wrote the implementation under those constraints.

Happy to take any question on the namespace design, the JP tokenizer choice, why I picked e5-large over BGE, or the LanceDB vs ChromaDB tradeoff.

— ぼぶ
```

---

## r/LocalLLaMA 固有の調整

| 項目 | HN v3 | r/LocalLLaMA 版 | 理由 |
|---|---|---|---|
| 冒頭 | "I built bobrain because..." | "Hey r/LocalLLaMA — sharing a small thing I built..." | sub の作法（コミュニティへの呼びかけ）|
| stack 詳細 | 1 段に圧縮 | 5 ブレットに展開 | embedding/vector DB ヲタ層への餌 |
| no Ollama / Docker | 暗示 | 明示 | 同 sub で頻出する地雷を踏まないため |
| Install ブロック | `pipx install bobrain` のみ | 3 行（index → index → serve） | 「実際に使える」を 1 秒で証明 |
| `**markdown bold**` | 控えめ | セクション見出しに使用 | Reddit は markdown 太字が読みやすい |
| LanceDB vs ChromaDB | 触れず | Q&A で誘発 | 同 sub の関心トピック |

---

## anti_patterns 6 カテゴリチェック

- カテゴリ 1: ✅ 思想言明なし
- カテゴリ 2: ✅ 「LangChain ベース」「OpenAI Embedding」言及なし
- カテゴリ 3: ✅ "no cloud round-trips, no telemetry" 強化
- カテゴリ 4: ✅ "便利" "高速" 不在、棄却の言明あり
- カテゴリ 5: ✅ 末尾「— ぼぶ」のみ、本文中はモード A
- カテゴリ 6: ✅ アプリツリー横断ルール抵触なし

---

## 投稿時の注意

- **self-promotion ルール**: r/LocalLLaMA は self-promotion 寛容だが、9:1 ルール（自分の投稿 1 に対し他者への参加 9）を非公式に守る空気あり。事前にコメント参加履歴があれば安心
- **タイミング**: r/LocalLLaMA のピーク時間は **米中部 9-11AM = 日本時間夜 23-1 時**（Show HN と同日 or 翌日推奨）
- **flair**: `[Resources]` or `[Discussion]` or `[Showcase]`（コミュニティガイドラインで確認）
- **HN との同時投稿は禁忌ではない**: 「Crosspost from HN」を明示しなければ、別投稿として通用
