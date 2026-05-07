# Awesome MCP PR 実行素材（PR 実行は人間トリガー）

**経緯**: punkpeye/awesome-mcp-servers の Knowledge & Memory section に bobrain を追加する PR の準備材料。実 README を取得して挿入位置・フォーマット・既存類似 entry を実地確認した結果。

**実行は人間トリガー**: 外部リポジトリへの PR は auto mode の対象外（projects/CLAUDE.md「Actions visible to others or that affect shared state: pushing code, creating/closing/commenting on PRs or issues」相当）。本ファイルはコマンド一式まで揃えて、ユーザーが各ステップを手動実行する想定。

---

## ターゲット section

**punkpeye/awesome-mcp-servers** > **🧠 Knowledge & Memory**

理由:
- 「Search & Data Extraction」「end to end RAG platforms」も候補だったが、bobrain は **個人の knowledge base を AI agent から扱う** 軸が中心、Knowledge & Memory が最適
- 同 section に既存類似 entry が複数（後述）→ 読者が比較しやすい
- README L1525 のセクション、約 160 entries

---

## 既存類似 entry（実地確認、競合認識用）

挿入時に PR レビュアー / 後続読者が比較する可能性が高い entry：

### 1. besslframework-stack/project-tessera（最も類似）
> Local workspace memory for Claude Desktop. Indexes your documents (Markdown, CSV, session logs) into a vector store with hybrid search, cross-session memory, auto-learn, and knowledge graph visualization. Zero external dependencies — **fastembed + LanceDB**, no Ollama or Docker required. 15 MCP tools.

→ **同じ stack（fastembed + LanceDB）+ hybrid search**。bobrain との差は: (a) **multi-root namespace**（project-tessera は単一 vault）, (b) **JP tokenization**, (c) **chunks-only / no summarization 哲学**

### 2. AliceLJY/recallnest
> Persistent memory MCP server for AI coding agents (Claude Code, Codex, Gemini CLI). Hybrid retrieval (vector + BM25), cross-encoder reranking, knowledge graph with PPR traversal, session checkpoint/resume, and **multi-scope isolation**. Local-first with **LanceDB + SQLite**.

→ multi-scope isolation = bobrain namespace と類似だが、recallnest は「coding agent のセッションメモリ」が中心、bobrain は「Obsidian + code repos の検索」が中心。**design center が違う**

### 3. bitbonsai/mcp-obsidian
mcpvault と同じ作者の別 entry、Obsidian only

---

## 挿入文（最終版）

```markdown
- [0916shokichi-blip/bobrain](https://github.com/0916shokichi-blip/bobrain) 🐍 🏠 🍎 🪟 🐧 - Local-first MCP server that indexes your Obsidian vault and your code repos as separate namespaces and queries across them in one hybrid search. BM25 with MeCab Japanese tokenization plus multilingual-e5-large dense embeddings, fused via reciprocal rank fusion. Returns chunks with file paths only — no summarization, no telemetry, no cloud round-trips. `pipx install bobrain`
```

### 絵文字 legend（README L46-72 で確認済み）

- 🐍 = Python
- 🏠 = Local Service
- 🍎 = macOS
- 🪟 = Windows
- 🐧 = Linux

bobrain は uv / Python 3.12 / pure Python 依存（OS 固有 binary なし）→ 全 OS 対応として 🍎 🪟 🐧 を付与可能。

### glama.ai badge

awesome-mcp の多くの entry が glama.ai badge を含む。bobrain は glama.ai に未登録なので **初版は badge なし**。後日 <https://glama.ai/mcp/servers> に submit して badge を付与する選択肢あり（必須ではない）。

---

## 挿入位置（README 内）

awesome-mcp は **アルファベット順を厳密に守っていない**（実地確認、`0xshellming/mcp-summarizer` が `Auctalis` の後に並んでいる等）。**実質的には追加順 or PR マージ順**。

→ **section の末尾に追加** が安全。alphabetical ordering で別の位置を要求されたらレビューで対応する。

具体的位置: README.md `## 🧠 Knowledge & Memory` section の最終 entry の後に新規行として追加。

---

## PR 実行手順（人間トリガー）

### 1. fork

```bash
gh repo fork punkpeye/awesome-mcp-servers --clone=false
```

(認証済み GitHub アカウントで fork が作成される)

### 2. clone & branch

```bash
mkdir -p ~/tmp/awesome-mcp-pr && cd ~/tmp/awesome-mcp-pr
gh repo clone 0916shokichi-blip/awesome-mcp-servers
cd awesome-mcp-servers
git checkout -b add-bobrain
```

### 3. README 編集

Knowledge & Memory section の末尾に上記の挿入文を追加。エディタで直接 or 以下のような sed:

```bash
# 末尾の entry を特定（別セクション開始の手前まで）→ 手動でエディタ推奨
$EDITOR README.md
```

挿入後、検索できることを確認:
```bash
grep -n "bobrain" README.md
```

### 4. commit & push

```bash
git add README.md
git commit -m "Add bobrain to Knowledge & Memory section"
git push origin add-bobrain
```

コミット author は projects/bobrain と同じく「ぼぶ <noreply>」になる前提。差異があれば mailmap 適用 or per-repo author 設定が必要（既知問題: bobrain CLAUDE.md L59）。

### 5. PR 作成

```bash
gh pr create \
  --repo punkpeye/awesome-mcp-servers \
  --title "Add bobrain to Knowledge & Memory" \
  --body "$(cat <<'EOF'
Adding bobrain — a local MCP server that indexes Obsidian vaults and code repos as separate namespaces, with hybrid BM25 + multilingual-e5 retrieval and Japanese tokenization out of the box.

What it adds vs existing entries in the section:
- Multi-root namespace design (most existing entries focus on a single vault or memory store)
- Japanese-aware BM25 by default (MeCab via fugashi + unidic-lite)
- chunks-only output, no summarization (returns chunk + file path)

Repo: https://github.com/0916shokichi-blip/bobrain
PyPI: https://pypi.org/project/bobrain/
License: MIT
EOF
)"
```

### 6. PR 後のフォロー

- PR が approved されない場合、レビュアーから「アルファベット順で並べ直して」「badge 追加して」「説明をもっと簡潔に」等の依頼が来る可能性
- 30 日以上 stale になったら polite に bump コメントを 1 回だけ
- レビュアーが他の awesome-mcp 系 list（wong2, appcypher）への登録を提案してきたら、それも検討

---

## 同時投稿戦略（リサーチ raw L #6 準拠）

リサーチ raw のアクション #6「MCP エコシステムへの積極的な相乗り」に従い、Tier 1 リストへ並列 PR：

1. **punkpeye/awesome-mcp-servers**（本ファイル）= 一次優先、最大規模
2. **wong2/awesome-mcp-servers** = 古参、二次優先
3. **appcypher/awesome-mcp-servers** = production-ready / experimental 区分あり、bobrain は experimental 行き

ただし `awesome-mcp-targets.md` の「PR 1 件ずつ慎重に」原則に従い、**punkpeye が approved or 24h 経過した後** に wong2 / appcypher へ進む。同時 3 PR は「prolific submitter」と見なされて却下されるリスク。

Tier 2（tolkonepiu/best-of-mcp-servers）は **PR 不要**（自動収集）。

---

## 想定インパクト

- punkpeye/awesome-mcp-servers は **GitHub star 50K+** クラスのコミュニティリスト
- マージされれば、bobrain への流入経路が 1 つ増える（特に Knowledge & Memory section を見る読者層）
- Show HN / r/LocalLLaMA / r/ObsidianMD と並行で進めれば、初動 24h で 4 経路の流入を期待可能
- ただし awesome list 経由の流入は HN ローンチほど bursty ではなく、長期 baseline 流入に近い性質
