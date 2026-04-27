# Bobrain — ローカル RAG MCP サーバー

「自分の脳を拡張する」ローカルファースト RAG MCP サーバー。Obsidian Vault と code repo の Markdown docs を横断検索できる MCP サーバー。マスコットは **Bob**（脳みそ + 丸メガネ + 栞付きノート、author ハンドル「ぼぶ」と一致）。

**リポジトリ**: https://github.com/0916shokichi-blip/bobrain （PUBLIC, MIT, author = ぼぶ）
**ローカルパス**: `~/projects/bobrain/`
**data dir**: `~/.bobrain/`
**戦略 wiki**: `/Users/higashishota/Documents/マネタイズ/`

## 過去の名前

2026-04-24 〜 2026-04-26 は「MyBrain MCP」+ マスコット「Mnemo」。ドメインが `mybrain` 系も `mnemo` 系も全 take + 作者ハンドル「ぼぶ」と一致させたく Bobrain にリブランド。詳細は `Documents/マネタイズ/log.md` の `[2026-04-26] decision | プロダクト名を Bobrain にリブランド + マスコットを Bob に` 参照。

## Why

- 知見習得最大化を最優先（RAG は AI エンジニアリング中核、MCP は業界標準プロトコル、Claude 以外のエージェントに横展開可能）
- ユーザー前提: 顔出し NG / 英語は Claude が訳す / 匿名運用 / 1 日 4 時間 / リスク大好き
- マネタイズ: コア OSS + 有料 Pro 版ハイブリッド（Lemon Squeezy 想定、MoR で顧客領収書に本名出ない）
- ターゲット: PKM パワーユーザー + 開発両刀（日本人多め）
- キラーメッセージ: 「探している答えは、何年か前のあなたが、もう書いている」（旧: 「Obsidian Vault と Git repo を同じ質問で検索できる」を 2026-04-27 に AgentCouncil ループで更新、L0 anti_patterns カテゴリ 4 違反だった機能羅列を体験文に置き換え）

## How to apply

- 開発再開時は `Documents/マネタイズ/log.md` の末尾を読んで最新状態を把握
- **Phase 1 完了 / Phase 3 #1 + #2 + #3 完了**（LP デプロイ + PyPI 0.1.0 公開済み、2026-04-27）。次は **Phase 3 #3 残タスク: GIF 撮影 + Social Preview 画像 + Show HN/Reddit 投稿** → **Phase 3 #4 決済**（NAWABARI / GMO / Polar.sh、人間アクション含む）
- LanceDB ≥ 0.30 で `db.list_tables()` は `ListTablesResponse(tables=[...])` wrapper、`.tables` 経由（`_table_exists` ヘルパ済み）
- 競合: [[Knowledge-RAG]]（最も近い）, [[Claude-Context]] (Zilliz, コード特化), [[Cognee]]（大規模・クラウド寄り）

## 現在地（2026-04-26 セッション終了時点）

### repo state

- visibility: PUBLIC, license: MIT, default branch: main, author 全コミット「ぼぶ <278669525+0916shokichi-blip@users.noreply.github.com>」
- description: 「Bobrain — a local-first multi-source RAG MCP server. Search your Obsidian vault and your repo's Markdown docs in one query, from Claude / Cursor / Claude Desktop. Hybrid BM25 + dense (multilingual-e5-large), Japanese-aware out of the box.」
- topics: `claude` `cursor` `embeddings` `japanese` `local-first` `mcp` `obsidian` `rag`
- 旧 URL `mybrain-mcp` は GitHub が redirect

### local state

- 未コミット変更なし、main は origin と同期
- 4 namespace index 揃い: `mybrain` (32, Phase 1 spike) / `monetize` (169) / `apptree` (306) / `claude-knowledge` (535) = 計 1042 chunks。namespace 名「mybrain」は spike 時の名残、必要時 rename 可能（既存検索は影響なし）

### 未対応の Phase 2 候補

- #3 `bobrain index` 複数ルート一括指定（cold start 15-30 秒）
- #5 `.bobrainignore` ファイルサポート
- #6 chunking が文字数ベース → Markdown heading 単位 chunking
- #7 e5-large が CPU で 1.4–2.4 sec/chunk → CoreML provider で 5-10x の余地

### ドメインメモ

- 旧名 `mybrain` 系（9 候補）と `mnemo` 系（14 候補）は `mnemo-mcp.com` 以外全 take
- **`bobrain` 系は 2026-04-26 確認**: `bobrain.com`（DNC Holdings、2000 年からの投機保有）と `bobrain.ai`（hostpoint.ch 運用中）以外、`.dev` `.app` `.io` `.sh` `.net` `.xyz` `.so` `.tools` `.page` `.run` および `usebobrain.com` `getbobrain.com` `trybobrain.com` `bobrainlabs.com` は **全部空き**。Pro 版販売開始時に `bobrain.dev` か `.app` 取得を検討
- 当面はドメインなしで `bobrain.vercel.app` か `<username>.github.io/bobrain` で LP 公開

### 匿名化メモ（Phase 3 #2 で実施済み、Bobrain 改称後も維持）

- git history は filter-repo で全 author/committer を「ぼぶ <noreply>」に rewrite 済み
- 残課題: GitHub アカウント名 `0916shokichi-blip` に「shokichi」が残る（rename コスト大、保留）
- mailmap: `/tmp/mybrain-mailmap.txt` は再起動で消える、再 rewrite 必要時はもう一度書く（1 行）

## 次回の作業順（Phase 3 #3 = LP、2026-04-26 セッション後の更新版）

### 2026-04-26 完了

- ✅ `bobrain` 系ドメインの whois 確認 → `.dev` `.app` `.io` `.sh` `.net` 等は空き、Pro 版前まではドメイン取らずに進む方針
- ✅ LP 構成案ドラフト（`marketer-ja` agent）→ 8 セクション + 日英バイリンガル + アクセント `#b14a3a`
- ✅ ベンチマーク数値整理 → 1042 chunks / 1.4-2.4 sec/chunk / ★ 評価をそのまま LP に
- ✅ **LP 実装完了 + 公開**: `~/projects/bobrain/docs/index.html`（単一 HTML、Playwright で動作確認済み、当初 `landing/` で作成 → GitHub Pages の publishing source 制約により `docs/` に rename）。Quickstart は `pipx install git+https://...` 初期表示、PyPI 公開後切替箇所は HTML コメントで marked
- ✅ **GitHub Pages 公開**: <https://0916shokichi-blip.github.io/bobrain/>（branch `main` / path `/docs`、`build_type=legacy`、HTTPS 強制、初回ビルドは数分）
- ✅ Bobrain グローバル展開戦略レポート（外部 Deep Research）を `Documents/マネタイズ/raw/` に取り込み、`research-ja` agent で事実検証 → `pages/analyses/Bobrain Phase 3-4 統合計画 — Polar 匿名事業基盤 2026-04-26.md` で評価

### 次回着手（順序更新）

1. **15 秒デモ GIF 撮影**（`screencapture` + `gifski`）: Claude Desktop で MCP 経由 search → notes と code namespace の両方からヒット → 15 秒。プライバシー上、Vault 名は demo/ 仕切りでダミー化推奨
2. **GitHub Social Preview 画像アップロード**（**user 操作必要**、`assets/og.png` を https://github.com/0916shokichi-blip/bobrain/settings から upload）
3. ~~PyPI 公開~~ → **完了 (2026-04-27)**: `bobrain 0.1.0` <https://pypi.org/project/bobrain/>。author = ぼぶ、Scope = Entire account の token で publish 済み
4. ~~LP の `pipx install bobrain` 切替~~ → **完了 (2026-04-27)**: `docs/index.html:880` と `README.md:36-43` の git+https 形式を `pipx install bobrain` / `uvx bobrain` に置き換え済み
5. ~~LP デプロイ~~ → **完了**（GitHub Pages 公開済み: <https://0916shokichi-blip.github.io/bobrain/>、4/26）
6. **Show HN / Reddit r/LocalLLaMA / r/ObsidianMD 投稿**（月曜火曜の米東部 6-8AM = 日本時間月曜夜 19-21 時、初動 90 分は Q&A に張り付き）

### Phase 3 #4（決済）の方針確定（2026-04-26 統合計画より）

- **MoR 第一候補: Polar.sh**（4% + $0.40、販売者表記「Polar Software Inc.」、GitHub ネイティブ統合、KYC は Stripe Identity）
- **MoR 予備: Lemon Squeezy**（5% + $0.50、Stripe 傘下、PayPal 対応が必要になったら併用）
- **バーチャルオフィス: NAWABARI**（月 1,100 円、**GPS 混入チェック実装済み**、留守電音声メール転送で肉声露出回避）
- **屋号: Bobrain Labs**（NAWABARI 契約時に屋号宛郵便受領可を同時依頼）
- **銀行: GMO あおぞらネット銀行 屋号付き口座**（Selfie 動画認証で即日に近いスピード、通常 1 週間）
- **特商法表記運用: 「請求があれば遅滞なく開示」**（`legal-ja` agent で雛形作成）
- 取り込まなかった外部レポート提案: 「思想的 README リライト」「赤ちゃんアバター動画オーバーレイ」は A/B モード分離 + アプリ固有キャラ 1 体原則に反するため不採用。詳細は `Documents/マネタイズ/pages/analyses/Bobrain Phase 3-4 統合計画 — Polar 匿名事業基盤 2026-04-26.md`

### スタイロメトリー対策（ローンチ告知前）

- 英語 README / Issue 返信は `humanizer-ja` で 1 回通す

### 参考コマンド

- 全 test: `cd ~/projects/bobrain && uv run python -m pytest -q`（16 cases。`uv run pytest` 直接は `.venv/bin/pytest` の shebang が古い `mybrain-mcp` path のままで動かない。`uv sync --reinstall` か `.venv` 削除 → `uv sync --dev` で解消）
- 横断検索: `uv run bobrain search "クエリ" -k 5 [--ns A --ns B]`
- repo metadata: `gh repo edit 0916shokichi-blip/bobrain --description ... --add-topic ...`
- author 再 rewrite（必要時）: `uvx git-filter-repo --mailmap mailmap.txt --force` の後 origin 再追加 + `git push --force-with-lease`

## L0 Taste Layer（評価関数の正本）

機能追加・LP コピー変更・Pro 版機能選定など、bobrain の「何を作るか / 作らないか」の判断は `.agents/director/` を参照する：

- `.agents/director/vision.md` — 提供すべき変容的体験（過去の自己との再会）
- `.agents/director/philosophy_os.md` — 上位 `cross_project_philosophy` への参照 + bobrain 固有の 3 観点
- `.agents/director/qdaif_axes.yaml` — 4 軸スコアリング（知行合一 / パラダイムシフト / 生産的摩擦 / 多様性）、閾値 14
- `.agents/director/anti_patterns.md` — 6 カテゴリの平凡化シグナル、該当時は QDAIF 評価以前に即却下

平凡化チェックは subagent `gamma-contrarian-ja`（明示起動）で叩く。詳細はアプリツリー wiki [[自律型開発スタジオの5層モデル]] 参照。

## 仮想 AI 会社構造

- CEO = ユーザー（意思決定・方向性・最終レビュー）
- 仮想 CTO = Opus 4.7（設計判断・難デバッグ）
- 仮想エンジニア = Sonnet 4.6（日常実装）
- 仮想ジュニア = Haiku 4.5（単純作業）
- 仮想デザイナー = `frontend-design` skill
- 仮想 QA = `test-thinker` + `code-reviewer-ja`
- 仮想リサーチャー = `research-ja` + `Explore` agent
- 仮想マーケター = `marketer-ja`
- 仮想法務 = `legal-ja`
- 仮想 DevOps = bash + hooks + launchd routines

## 技術スタック

Python 3.12 + uv + mcp (FastMCP) + lancedb + fastembed + rank-bm25 + typer + pymupdf + watchdog + tqdm。src layout、CLI 名 `bobrain`、パッケージ名 `bobrain`、Python モジュール `bobrain`。

## Phase 0/1/3#1/3#2 で完了したもの（再度やらない）

- Phase 0: SaaS テーマ確定、競合調査、技術スタック確定、MVP スコープ、GitHub リポ作成、spike feasibility、Mnemo キャラ（後に Bob に置換）
- Phase 1: e5-large embedding、MeCab BM25、watchdog incremental、MCP E2E テスト
- Phase 3 #1 ドッグフーディング: `--exclude` CLI + dim auto-migration、tqdm + phase timing、3 wiki index、検索品質評価
- Phase 3 #2 公開: 匿名性監査、author rewrite、Mnemo OG 画像、README pipx 追記、CONTRIBUTING / .github / CODE_OF_CONDUCT 整備、PUBLIC 化、description / topics 整備、Bobrain リブランド + Bob マスコット作成 + GitHub repo rename

---
_2026-04-26 に `~/.claude/.../memory/bobrain_project.md` から移行_
