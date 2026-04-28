# r/ObsidianMD 派生 draft（v3 ベース、PKM コミュニティに合わせて調整）

**経緯**: Show HN v3 (`show-hn-final.md`) を r/ObsidianMD 用に調整。
- PKM サブレディットの作法: 機能スパムは即 downvote、自分のワークフロー文脈で語る、商用感を薄く
- HN との差: HN は技術スタックが評価軸、r/ObsidianMD は「Obsidian ユーザーとしての困りごと」が評価軸
- self-promotion 厳格: 投稿前に sub のルール確認必須

---

## タイトル候補

### 推奨: R-OBS-1
> I built an MCP that searches my Obsidian vault and my code READMEs together (local, no plugin)

- 「I built X for Y」= sub の作法
- 「no plugin」を明示 → Local REST API plugin 必須の既存 MCP との差別化
- 「code READMEs」は r/ObsidianMD 読者に伝わりやすい（具体例）

### 代替: R-OBS-2
> A local MCP server that lets Claude search my Obsidian vault alongside my code repos

- より控えめなトーン

---

## 本文

```
Hi r/ObsidianMD — I want to share something I built that maybe scratches an itch some of you have too.

I've been writing notes in Obsidian for years. But the thing is, half of my "knowledge" isn't in my vault — it's in the READMEs and `docs/` folders of every code project I've worked on. When I'd ask Claude (via MCP) about something, it could only see one of those at a time. I kept hitting "I know I wrote this somewhere" with no way to search both.

So I made bobrain. It's a local MCP server that indexes your Obsidian vault and any number of other folders (like ~/code/) as separate namespaces, and lets your AI client (Claude, Cursor, Claude Desktop) search across all of them in one query.

**How it differs from existing Obsidian MCPs**

I checked the alternatives — engraph, obsidian-brain, vaultforge, mcpvault, and the REST API plugin-based servers (mcp-obsidian, obsidian-mcp-tools). They're all Obsidian-only. bobrain is the multi-root one.

It also doesn't need Obsidian to be running, and doesn't need the Local REST API plugin installed. It just reads .md files from disk. So your vault is just a folder of files, the way it actually is.

**What's in it**
- Hybrid search (BM25 + dense embeddings, fused with reciprocal rank fusion)
- Japanese-aware out of the box (MeCab tokenizer, since some of my notes are JP)
- Multiple folders as separate namespaces, queryable independently or together
- Watch mode that reindexes as you edit
- 100% local — no cloud, no telemetry, embeddings run on your machine

**What it's not**
- not a chatbot, not a summarizer — it returns chunks with file paths, your LLM does the rest
- not an Obsidian plugin (it's a separate process)
- not a replacement for Obsidian's built-in search; it's for AI clients to query your knowledge

**How it works in practice**
```
pipx install bobrain
bobrain index ~/Documents/MyVault -n vault
bobrain index ~/code -n code
bobrain serve
```

Then point Claude / Cursor / Claude Desktop at it as an MCP server.

**Repo**: https://github.com/0916shokichi-blip/bobrain (MIT, early prototype)

Solo project. Honest disclosure: I wrote the design and tests, Claude Code wrote the implementation. Commits are unsquashed if you want to read the trail.

Curious to hear how others handle this gap — especially anyone who's been mixing Obsidian with their code workflow. And happy to take any question on the namespace design or why I picked e5-large for embeddings.

— ぼぶ
```

---

## r/ObsidianMD 固有の調整

| 項目 | HN v3 | r/ObsidianMD 版 | 理由 |
|---|---|---|---|
| 冒頭 | "I built bobrain because..." | "Hi r/ObsidianMD — I want to share something..." | sub の作法（やわらかい入り） |
| 困りごとの具体性 | "my notes and my code aren't in the same place" | "READMEs and docs/ folders of every code project" | PKM ユーザーが想像しやすい例 |
| 競合言及の重み | 1 段で 4 個列挙 | 「checked the alternatives」と謙虚に + REST API plugin 系も追加 | sub の文脈ではこちらが網羅的 |
| MCP 用語 | 自然に使う | 説明的に使う（「a separate process」「your AI client」） | r/ObsidianMD は MCP 知らないユーザーも多い |
| Stack 名 | BM25 + e5 + RRF + MeCab を 1 行 | 4 ブレットに分解 + 用語を控えめに | 技術ヲタ層へではなく PKM 層への訴求 |
| not 段 | 行動の記述 | 「not a X, not Y」3 連 | 期待値マネジメント |
| 締め | "Happy to take any question" | "Curious to hear how others handle this gap" | コミュニティへの問いかけ（discussion 誘発） |
| Disclosure | "Solo project. Design and tests are mine..." | "Honest disclosure: I wrote the design and tests..." | sub の作法（"honest" は r/ObsidianMD で頻出） |

---

## anti_patterns 6 カテゴリチェック

- カテゴリ 1: ✅ 思想言明なし
- カテゴリ 2: ✅ 「Mem.ai」「Notion AI」「Smart Connections」言及なし、競合語彙避ける
- カテゴリ 3: ✅ "100% local — no cloud, no telemetry" 強化
- カテゴリ 4: ✅ "便利" "高速" 不在、"not a chatbot, not a summarizer" 棄却の言明
- カテゴリ 5: ✅ 末尾「— ぼぶ」のみ
- カテゴリ 6: ✅ アプリツリー横断ルール抵触なし

---

## 投稿時の注意

- **self-promotion ルール**: r/ObsidianMD は self-promotion 厳格、サブレディットルールを **投稿前に再確認必須**
- **flair**: r/ObsidianMD には `Showcase` `Plugins` `Other Tools` などの flair あり、最も近いのは `Other Tools`（プラグインではないため）
- **タイミング**: r/ObsidianMD のピーク時間は **欧州夜 + 米東部 9-11AM = 日本時間夜 22-24 時**
- **HN / r/LocalLLaMA との差別化**: 同日に 3 sub 投稿しても OK だが、各投稿が **ターゲット sub の語彙で書かれている** ことが重要（テンプレ転用は即バレる、既に v3 から sub ごとに調整済み）
- **コメント返信**: r/ObsidianMD は技術的回答だけでなく「workflow の語り合い」を喜ぶ。「I tried X for Y, it didn't work because Z」のような体験談を共有する形でコメント返信すると好印象
