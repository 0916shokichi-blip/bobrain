# r/ObsidianMD 派生 draft（v3 ベース、PKM コミュニティに合わせて調整）

**経緯**: Show HN v3 (`show-hn-final-v3.md`) を r/ObsidianMD 用に positioning 揃え。
- PKM サブレディットの作法: 機能スパムは即 downvote、自分のワークフロー文脈で語る、商用感を薄く
- HN との差: HN は技術スタックが評価軸、r/ObsidianMD は「Obsidian ユーザーとしての困りごと」が評価軸
- self-promotion 厳格: 投稿前に sub のルール確認必須
- **v3 positioning 整合**: README/LP hero「The answer you're searching for — you already wrote it, years ago.」と post 冒頭が echo する構造を維持。「半分は Vault、半分は README」の旧具体 → 「years ago に答えてた」軸へ抽象化

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
Hi r/ObsidianMD — sharing something I built because I kept asking my AI assistant (via MCP) questions I'd already answered years ago. Half the time the answer was in a note I'd forgotten about, the other half it was in the README of some long-archived repo. There was no way for Claude to surface either.

bobrain is a local MCP server that gives your AI client access to those layers. Point it at your vault, ~/code/, anything markdown or source on disk — it indexes each as a separate namespace. One query hits all of them.

  Q: "How did I think about retry/backoff in any past project?"

  → bobrain returns:
    • a chunk from reliability-notes.md (2023)
    • the actual exponential-backoff implementation from a 2022 repo
    • a related Slack paste in my Obsidian inbox

**Why it's a separate process, not a plugin**

It reads .md files straight from disk. Obsidian doesn't need to be running, and you don't need the Local REST API plugin installed. Your vault is just a folder of files — bobrain treats it that way.

**What's in it**
- Hybrid search: BM25 + multilingual-e5-large dense embeddings, fused with reciprocal rank fusion
- Japanese-aware out of the box (MeCab tokenizer, since some of my notes are JP)
- Multiple folders as separate namespaces, queryable independently or together
- Watch mode that reindexes as you edit
- 100% local, in-process via ONNX. No telemetry. Not even error reporting.

**Two things it deliberately doesn't do**
- summarize what comes back. You see the raw chunk + file path. When you're trying to recall what past-you actually wrote, paraphrase is the enemy.
- send your notes anywhere. Embeddings run on your machine. The point is your knowledge stays on your disk.

**How it works in practice**
```
pipx install bobrain
bobrain index ~/Documents/MyVault -n vault
bobrain index ~/code -n code
bobrain serve
```

Then point Claude / Cursor / Claude Desktop at it as an MCP server.

**Repo**: https://github.com/0916shokichi-blip/bobrain (MIT, early prototype)

Honest disclosure: solo project, I wrote the design and tests, Claude Code wrote the implementation. Commits aren't squashed if you want to read the trail.

Curious to hear how others handle this gap, especially anyone who's been mixing their Obsidian workflow with their code repos. Happy to take any question on the namespace design, the JP tokenizer choice, or why a separate process beat a plugin for this one.

— ぼぶ
```

---

## r/ObsidianMD 固有の調整（v3 ベース）

| 項目 | HN v3 | r/ObsidianMD 版 | 理由 |
|---|---|---|---|
| 冒頭 | "I keep asking my AI coding assistant questions I already answered years ago" | "Hi r/ObsidianMD — sharing something I built because I kept asking my AI assistant questions I'd already answered years ago" | sub の作法（コミュニティへの呼びかけ）+ v3 核 punch 維持 |
| 具体例 | "forgotten Obsidian note, or a README from a long-archived repo" | 同（PKM 層に直結） | r/ObsidianMD は Vault 文脈で読むので原文ママで通る |
| Example query | 3 result の構造体 | 同 | v3 で確立した「過去の自分との対話」を直接書かず体現する核心装置、媒体差で変えない |
| plugin vs process | 暗示 | 1 段独立（"Why it's a separate process, not a plugin"）| r/ObsidianMD はプラグイン文化、敢えて plugin じゃない理由を明示 |
| Stack 名 | 1 段に圧縮 | 5 ブレットに展開 | 技術ヲタ層ではなく PKM 層への訴求、用語は控えめ |
| 「N things doesn't do」 | Two | **Two**（v3 整合）| self-help 三点セット軸 3 弱化、HN/r/LocalLLaMA と統一 |
| Privacy line | "No telemetry. Not even error reporting." | "100% local, in-process via ONNX. No telemetry. Not even error reporting." | 1 行に集約、独立 punch |
| 締め | "Happy to dig into the namespace design..." | "Curious to hear how others handle this gap... Happy to take any question on..." | コミュニティへの問いかけ（discussion 誘発）+ Q&A 誘導の二段 |
| Disclosure | "Solo project. Design and tests are mine..." | "Honest disclosure: solo project, I wrote the design and tests..." | sub の作法（"honest" は r/ObsidianMD で頻出） |

---

## anti_patterns 6 カテゴリチェック

- カテゴリ 1: ✅ 思想言明なし（「映す世界を間違えた」直書きなし、Example query の暗示のみ）
- カテゴリ 2: ✅ 「Engraph」「obsidian-brain」「vaultforge」「mcpvault」「Mem.ai」「Notion AI」「Smart Connections」競合名指しゼロ
- カテゴリ 3: ✅ "100% local, in-process via ONNX. No telemetry. Not even error reporting." 独立 punch line
- カテゴリ 4: ✅ "便利" "高速" 不在、Two things で「summarize しない / send しない」棄却の言明
- カテゴリ 5: ✅ 末尾「— ぼぶ」のみ、本文中はモード A
- カテゴリ 6: ✅ アプリツリー横断ルール抵触なし

---

## 投稿時の注意

- **self-promotion ルール**: r/ObsidianMD は self-promotion 厳格、サブレディットルールを **投稿前に再確認必須**
- **flair**: r/ObsidianMD には `Showcase` `Plugins` `Other Tools` などの flair あり、最も近いのは `Other Tools`（プラグインではないため）
- **タイミング**: r/ObsidianMD のピーク時間は **欧州夜 + 米東部 9-11AM = 日本時間夜 22-24 時**
- **HN / r/LocalLLaMA との差別化**: 同日に 3 sub 投稿しても OK だが、各投稿が **ターゲット sub の語彙で書かれている** ことが重要（テンプレ転用は即バレる、既に v3 から sub ごとに調整済み）
- **コメント返信**: r/ObsidianMD は技術的回答だけでなく「workflow の語り合い」を喜ぶ。「I tried X for Y, it didn't work because Z」のような体験談を共有する形でコメント返信すると好印象
