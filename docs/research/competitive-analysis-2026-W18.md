---
date: 2026-05-01
status: draft
source: github-trending-radar W18 synthesize (commit 2236bc6)
purpose: Show HN 投稿前の差別化 axis 確定 + Phase 3 設計判断の根拠
---

# Bobrain 競合分析 W18 — 機能 overlap と差別化 3 軸

## なぜこの分析が必要か

Show HN 投稿前に「**他と何が違うのか / 何が同等なのか**」を実数で言える状態にする。「How it performs draft v1」が playable-gate で却下された理由（DR 提案「実数表型訴求」が業界標準テンプレート化していて Gamma が平凡判定、memory `showhn_launch_benchmarks_2026.md`）を踏まえて、本分析は **「実数表で差別化を訴求する」のではなく「設計思想の対立軸を言語化する」** ことに重きを置く。

## 比較対象（github-trending-radar W18 で発見）

| repo | ★ | 言語 | 直近 push | 警戒度 |
|---|---|---|---|---|
| **kiwifs/kiwifs** | 245 | Go 1.25 | 2026-04-30 | **🔴 同概念競合** |
| **alash3al/stash** | 592 | Go | 2026-04-29 | 🟡 機能直競合 |
| **aeroxy/ast-outline** | 100 | Rust | 2026-04-30 | 🟢 思想対立、設計示唆 |

## 機能 overlap 表

| 軸 | bobrain | kiwifs | stash | ast-outline |
|---|---|---|---|---|
| **言語** | Python 3.12+ | Go 1.25 | Go | Rust |
| **ライセンス** | MIT | **BSL 1.1**（4 年後 OSS、商用条件） | Apache-2.0 | MIT |
| **インストール** | `pipx install bobrain` | `curl install.sh \| sh` (single binary) | `git clone + docker compose up` | `brew install` / `cargo install` |
| **依存** | Python + ONNX + 約 2.2GB e5 weights | **none** (single Go binary) | **Postgres + pgvector** | **none** (single Rust binary) |
| **データ層** | LanceDB (SQLite-based) | SQLite FTS5 | Postgres | stateless |
| **検索** | **BM25 (MeCab) + dense (e5-large) + RRF** | FTS5 (BM25) + pluggable vector | pgvector | (検索なし、AST outline のみ) |
| **書き込み** | ❌ read-only | ✅ agents write via cat/echo/MCP | ✅ episodes consolidate to facts | ❌ read-only |
| **多言語対応** | **🟢 Japanese-aware (MeCab fugashi+unidic)** | 🟡 FTS5 default、CJK 弱い | 🟡 pgvector default、CJK 弱い | 🟢 10 言語 AST (Rust/C#/Python/TS/JS/Java/Kotlin/Scala/Go/Markdown) |
| **Web UI** | ❌ なし（CLI/MCP only） | ✅ wiki / graph view / backlinks | ❌ docs サイトのみ | ❌ CLI only |
| **MCP server** | ✅ stdio | ✅ あり | ✅ あり | ❌ なし（CLI tool） |
| **思想 / 個性** | 「探している答えは、何年か前のあなたが、もう書いている」 | 「LLM Wiki pattern」「files are the truth」 | 「Your AI has amnesia. We fixed it」 | 「Pre-reading layer」「files not embeddings」 |
| **Pricing 計画** | OSS + Pro (Polar.sh 想定) | OSS + 商用 BSL | OSS のみ（明示） | OSS のみ |
| **公開ステータス** | 0★ 0fork 未投稿 | 245★ active | 592★ active | 100★ active |

## 差別化 3 軸（実数 + 設計思想）

### A. Japanese-aware を default に持つ唯一の選択肢

- bobrain: `fugashi + unidic-lite` で **MeCab tokenize がデフォルト**。日本語の検索精度が `BM25(MeCab) + dense(multilingual-e5)` のハイブリッドで設計時から考慮されている
- kiwifs: SQLite FTS5 default = **CJK では空白区切りに依存**、日本語は事実上動かない。pluggable vector に embeddings を入れても、BM25 側が無力
- stash: pgvector default = embeddings 単独。CJK BM25 補強は外付け必要
- **実数**: bobrain index で日本語 markdown を投げて MeCab トークナイズした BM25 hit 数 vs kiwifs の FTS5 hit 数を比較すれば、検索 recall が桁違いに違う見込み（要 benchmark、Show HN 前に 1 つだけ実測しておくと "How it performs" v2 の素材になる）

### B. 「過去の自分との再会」という体験 framing（philosophy_os と人格紐付け）

- bobrain: 「探している答えは、何年か前のあなたが、もう書いている」= **時間軸を遡る体験**。マスコット Bob（脳みそ + 丸メガネ + 栞付きノート）+ 作者人格「ぼぶ」と紐付き、philosophy_os「映す世界を間違えた」の表現として設計
- kiwifs: 「Virtual filesystem agents can write, search, query, and trust」= **Agent 視点の機能羅列**、人格不在
- stash: 「Your AI has amnesia. We fixed it」= 病気の比喩、「治った」という二項対立、感情温度は中性
- ast-outline: 「pre-reading layer」= 純技術名、感情ゼロ
- **差別化**: bobrain は唯一「**ユーザー自身が過去の自分と出会う**」体験を中心に置いている。これは memory `cross_project_philosophy.md` の「世界ではなく解釈を変える」と直結する独自軸（kiwifs は「ファイルを信頼せよ」、stash は「AI に記憶を与える」で、いずれも user 自身の世界観への作用は語らない）

### C. Python エコシステム + Obsidian Vault パワーユーザーへの引き

- bobrain: `pipx install bobrain` 1 行。Python ユーザーが local-first で Obsidian Vault と git repo を **横断検索** したい時の最短経路
- kiwifs: Go binary で言語非依存だが、自分の既存 Vault を index する経路ではなく **新しい kiwifs フォルダに init する設計**（serve --root ./knowledge）。既存の Obsidian Vault を直接 mount できるかは README から不明（要 docs 確認）
- stash: docker compose up + Postgres + .env 編集 = **エンタープライズ志向のセットアップ**。個人の Vault に向けるツールではない
- **差別化**: bobrain は「**既存の Obsidian Vault の上に薄く乗る**」。新たな folder structure を導入しない。Python パワーユーザー + 既存 Vault + 「Vault と code repo を同じ質問で検索」という具体使用文脈が刺さる

## 致命的な弱点（正直に言語化）

### 弱点 1: Web UI / 書き込み機能の不在（kiwifs に劣後）

kiwifs は agents が **cat/echo/MCP で書き込み可能** + **Web UI（wiki / graph / backlinks）** を提供。bobrain は read-only な検索 + MCP のみ。「Obsidian アプリを使えばいい」と割り切っているが、kiwifs ユーザーから見ると bobrain は機能的に劣後する。

**対応方針**: bobrain の position は「**index 専用**、UI は Obsidian アプリに任せる**unix philosophy 的な分業**」と明示する。kiwifs は VFS 全機能を内包する「monolithic LLM Wiki engine」。philosophy が違う。Show HN コピーで「we don't replace your editor — we extend it」を伝える方向。

### 弱点 2: ast-outline 思想（「embedding は ROI 低い」）の浸透リスク

ast-outline は明確に **「Modern agentic coding tools explore codebases by reading files directly — not via embeddings or vector search」** と書いている。この思想が広がると bobrain の embedding 中心戦略は陳腐化リスク。

**対応方針**: bobrain の使用文脈は **「コード探索のための AI agent」ではなく「PKM パワーユーザーの記憶横断」**。これは ast-outline の対象外（ast-outline は「コード agent が file を読む前段の outline」）。両者は **共存可能**（bobrain で意味検索 → kiwifs / Obsidian で書き込み → ast-outline でコード構造把握）。Show HN で「これは何向けじゃないか」を明示する（"not a code agent search tool"）。

### 弱点 3: 起動コストの重さ（first-run 2.2GB ダウンロード）

bobrain first run = `multilingual-e5-large` ONNX 約 2.2GB ダウンロード。kiwifs / stash は ML weights なし（kiwifs は pluggable vector で外付け、stash は pgvector で OS 経由）。**初回体験が重い**。

**対応方針**: README / LP に「First run downloads ~2.2GB」を明記済み。Phase 2 で `--lite` mode（embeddings なし、BM25 のみ）を出すと初学者の入り口が軽くなる候補。Phase 3 #7 (CoreML provider) でランタイム速度の差別化はカバーされる予定。

## ast-outline の設計示唆（CLAUDE.md L48 #6 chunking 戦略への apply）

bobrain CLAUDE.md L48 既知課題: **「#6 chunking が文字数ベース → Markdown heading 単位 chunking」**。ast-outline は AST 単位で構造を返すツールで、これを bobrain chunker に直接 import するのは不適合（bobrain は Markdown 中心、ast-outline は code 中心）。

ただし **設計思想として** 「文字数ベース < 構造単位」は一致。bobrain Phase 3 で実装する場合、AST のような正確性ではなく **Markdown heading レベル + length budget** の hybrid chunking が現実的（既に Phase 2 候補 #6 にある通り）。ast-outline は「コードファイルを bobrain index する場合の前処理」として将来統合候補（"namespace=code" モードで AST chunking、"namespace=notes" モードで Markdown heading chunking の dispatcher）。

**Phase 3 への結論**: 即 ast-outline を pip install して試すのは早い。Markdown heading 単位 chunking を先に実装、その後 code namespace 向けに AST chunking を追加する 2 段階が筋。本分析の範囲では試用までは行わない。

## Show HN コピーへの素材（"How it performs" v2 用）

実数表ではなく **「他と何が違うのか / 何が同等なのか」** を 3 行で言える素材:

> Bobrain 0.1.0 is a **read-only index layer** for people who already trust their Obsidian Vault and their git repos. It is not a virtual filesystem (like KiwiFS) and not an agent memory consolidator (like Stash). It is **the missing index** when your knowledge already lives in markdown files and you want to search across them — including code repos — in Japanese, locally, from any MCP-compatible client.
>
> "The answer you're searching for — you already wrote it, years ago."

**playable-gate 通過の鍵**: anti_patterns カテゴリ 4 違反（機能羅列）を避けつつ、kiwifs / stash と明確に **「これではない」** を言うこと。「我々は何を引き受けて、何を引き受けないか」を率直に書く（**stash の 50 行 README に学ぶ**: stash は機能を 8 stage consolidation pipeline と言いつつ、その詳細は別ページに切り出して、README は「your AI has amnesia. we fixed it.」+ Quick Start で完結）。bobrain も Show HN 投稿テンプレで同じ筋を狙う。

## 実装 TODO（Phase 3 #3 / #4 を超えて）

- [ ] **Show HN 投稿後**: BSL 1.1 vs MIT を再考（OSS 認定主張可否、kiwifs が BSL 1.1 で実験中）
- [ ] **Phase 3 #6 着手時**: Markdown heading 単位 chunking 実装、ast-outline 思想は "code namespace" モードの将来候補としてメモ
- [ ] **README 更新（Show HN 前）**: 「we don't replace your editor — we extend it」「not a code agent search」「Japanese-aware out of the box」の 3 行を導入文に追加
- [ ] **日本語検索の実数 1 つ取る**: bobrain で日本語 markdown を index → 同じクエリで kiwifs FTS5 と recall 比較（1 サンプルで OK、Show HN コピーで使える素材）

## 結論（差別化 3 軸の総括）

bobrain の **唯一無二** は次の重なり点:

1. **Japanese-aware (MeCab) BM25 + dense hybrid** が default
2. **「過去の自分との再会」体験 framing**（philosophy_os と人格紐付け）
3. **既存 Obsidian Vault に薄く乗る**（新フォルダ強制なし、Python pipx 1 行）

この 3 軸の重なる人は「**日本語で書く Obsidian パワーユーザーで、Python エコシステムに居て、ローカル完結を望み、過去の自分と再会したい人**」。狭いが鮮明。kiwifs / stash / ast-outline はいずれもこの重なりを持っていない。Show HN ではこの 3 軸の **重なり** を訴求する（個別の 3 軸を訴求すると業界平均値の機能羅列に戻る）。
