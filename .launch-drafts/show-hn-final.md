# Show HN 最終版（コピペ用、playable-gate v3 通過済み）

**経緯**: v3 が playable-gate を通過（anti_patterns 全クリア / Gamma 構造攻撃を経て / QDAIF 15.8 / L4 人間関門 YES）。本ファイルは投稿時にそのままコピペできる純粋な最終版。詳細な設計判断と評価記録は `show-hn-draft.md` を参照。

---

## タイトル（76 文字）

```
Show HN: bobrain – A local MCP that searches my notes and code repos together
```

## 本文

```
I built bobrain because my notes and my code aren't in the same place. The notes I've been writing for years live in ~/Documents/notes/ as Obsidian markdown; every solved engineering problem is buried in the README of some old ~/code/<project>/. I kept hitting "I know I wrote this somewhere" with no way to search across both.

bobrain is a local MCP server that indexes both, as separate namespaces, and lets your AI client (Claude / Cursor / Claude Desktop) query across all of them at once. It uses BM25 with MeCab Japanese tokenization (some of my notes are Japanese) plus multilingual-e5-large dense embeddings, fused with reciprocal rank fusion. Everything runs in-process; no telemetry, no cloud round-trips.

Existing Obsidian MCP servers are great at one vault — engraph for knowledge graphs, obsidian-brain for PageRank, vaultforge for Canvas, mcpvault as a universal bridge. None of them index code repos alongside the vault. bobrain is a multi-root one.

Three things it does not do, by design:
- summarize the chunks for you. What comes back is the chunk and the file path, nothing else
- send your notes anywhere — embeddings run via in-process ONNX
- require Obsidian to be running. Plain .md files on disk is enough

Solo project. Design and tests are mine; commits are not squashed if you want to read along. Claude Code wrote the implementation under those constraints.

Repo: https://github.com/0916shokichi-blip/bobrain
LP: https://0916shokichi-blip.github.io/bobrain/
Install: pipx install bobrain

Happy to take any question on the namespace design, the JP tokenizer choice, or why I picked e5-large over BGE.

— ぼぶ
```

---

## 投稿前チェックリスト

- [ ] **`humanizer-ja` を通す**: projects/CLAUDE.md L94 スタイロメトリー対策。`humanizer-ja` skill で本文を 1 回通してから投稿
- [ ] **GitHub Social Preview 画像**: bobrain CLAUDE.md L76 残タスク。投稿前に `assets/og.png` を <https://github.com/0916shokichi-blip/bobrain/settings> から upload。投稿経由訪問者が repo 画面を見たときの第一印象
- [ ] **15 秒デモ GIF**: bobrain CLAUDE.md L75 残タスク。本文中にリンク追加するなら作成（本文にリンクなしでも OK、README に貼っておけば十分）
- [ ] **GitHub repo description 確認**: 既に整備済み（CLAUDE.md L34）、念のため最新版を repo settings で確認
- [ ] **PyPI 0.1.0 が `pipx install bobrain` で動くことを別マシン or fresh venv で確認**: 投稿後に「動かない」と言われると致命的

---

## 投稿タイミング

**HN 黄金時間帯**: 火曜火曜 6-8AM EST = 日本時間 **月曜・火曜の夜 19-21 時 (JST)**
- HN front page は最初の 1-2 時間で 10 ポイント獲得が条件
- ローンチ後 90 分は Q&A に張り付く前提でスケジュール確保
- bobrain CLAUDE.md L80 の現行方針と一致

**避けるべき時間帯**: 金曜午後 / 土日（コミュニティ流入が落ちる、初動 10 ポイントを取りにくい）

---

## 投稿後の Q&A 想定（FAQ ドラフト）

### Q1: なぜ LangChain ではなく自前実装？
> 設計判断としてシンプル。LangChain を入れると依存関係が肥大化し、ローカル前提（ONNX in-process）の設計と整合しない。BM25 (rank-bm25) + fastembed + LanceDB の 3 つだけで構築。1042 chunk index で起動・検索ともに sub-second。

### Q2: なぜ e5-large over BGE?
> 多言語対応（multilingual-e5）が必要だったため。BGE-m3 も候補だったが、e5 の query/passage prefix が design center（過去の自分の言葉と現在のクエリは異なる文体）と整合した。BGE への置き換えはユーザー側で `EMBEDDING_MODEL` env で可能（roadmap）。

### Q3: なぜ要約しない？
> 要約は呼び出し側 LLM の責務。bobrain は chunk と file path を返すだけ。これは「ユーザーが過去の自分の言葉を、要約越しではなく原文で読む」設計。

### Q4: code repo 横断は具体的にどう違う？
> namespace 機能。`bobrain index ~/Documents/notes -n notes` と `bobrain index ~/code/myproject -n code` を別 namespace として登録 → クエリ時に `--ns notes --ns code` で横断 or 単独。各 namespace は独立した index、衝突しない。

### Q5: Pro 版は？
> Phase 4 で検討中（決済プロバイダ Polar.sh 想定）。Pro 版でもクラウド送信機能は **作らない**（philosophy_os の core）。チーム機能 / 高度な分析 / 業務統合の方向のみ。

### Q6: Vibe-coded ですか？
> いいえ。設計判断・テスト・トレードオフは私が行い、Claude Code は実装担当。commit history は unsquashed なので、設計と実装の分離は読み取れる。

### Q7: 日本語以外でも動く？
> はい。MeCab tokenizer は日本語 path のみ active、英語の chunk は通常通り BM25 + e5 で処理。multilingual-e5-large は 100+ 言語対応。

---

## 投稿後の張り付き原則（projects/CLAUDE.md モード A 整合）

- 最初 12 時間は **モード A（中立・技術的）** で全質問即答
- 24 時間後に議論が深まったら、bob-universe の連続性をさらりと匂わせる程度（モード B には踏み込まない、Show HN は商用 PR の場、思想モードは philosophy-chat 本体）
- 「why local?」系の質問には philosophy_os L26 を行動として記述（「自分の脳のデータを他人の API に預けない」を直接書かず、「embeddings run in-process, that's the whole stack」のように体現）
- 競合作者からコメントが来たら誠実に「your hero copy から要約しました」（vaultforge 比較表と同じ作法）

---

## 並行投稿（Reddit）

同日 or 翌日に並行投稿する派生バージョンは別ファイル：
- `reddit-localllama.md` — r/LocalLLaMA 用（技術詳細厚め、cloud バッシング軽く）
- `reddit-obsidianmd.md` — r/ObsidianMD 用（PKM 文脈、商用感弱め）
