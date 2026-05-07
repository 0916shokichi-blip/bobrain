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
  - **強制方法**: local git config で匿名固定（`git config user.name "ぼぶ"` + `git config user.email "278669525+...@users.noreply.github.com"`）。global config が本名でも local が優先。新規 clone / 環境再構築時に必ず再設定。2026-04-28 に config 漏れで本名 commit を 5 件作って force push 復旧した教訓は memory `bobrain_pypi_launch.md` 第 5 の地雷参照
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
6. ~~共通フッター規格 (N=1) 適用~~ → **完了 (2026-04-28)**: README.md と docs/index.html の footer を `bob_persona.md` の共通フッター規格に揃えた。Avatar by Nano Banana Pro の理由付き disclosure + `1 of 8 tools` クロスリンク（暫定 link 先 = GitHub プロフィール、bob-universe デプロイ後に bob_persona.md 1 箇所更新で全アプリ伝播）
7. **Show HN / Reddit r/LocalLLaMA / r/ObsidianMD 投稿** → 投稿前の最終ゲート + 投稿後の if-then は本ファイル「**Show HN 投稿の判断ロジック**」参照（後段）

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

## Show HN 投稿の判断ロジック

bobrain Show HN（および r/LocalLLaMA / r/ObsidianMD）投稿時の if-then 判断ロジック。memory `showhn_launch_benchmarks_2026.md` の定量基準 + `vibe_maintainer_disclosure.md` の開示型 4 分類 + bobrain L0 anti_patterns を bobrain 固有の状況に落とし込んだ運用ルール。**transcribe-bird など他 OSS の Show HN にもそのまま再利用可**（本セクションをコピーして project 固有値だけ書き換える）。

### 投稿前の最終ゲート（D-1 〜 D-0、全部満たさないと投稿しない）

- [x] `.launch-drafts/show-hn-draft.md` 最新版が `/playable-gate bobrain --target .launch-drafts/show-hn-draft.md` で **anti_patterns 該当なし** + Gamma 平凡化攻撃 通過（v3 は通過済み 2026-04-28）
- [x] **README に「How it performs」「What this is, and what it isn't」相当の中盤訴求セクションを置かない方針確定（2026-05-01）**。v1（実数表型）/ v2（境界線型）両方が playable-gate Gamma で却下 — 前者は anti_patterns カテゴリ 4「機能比較表の数値競争」直撃、後者は OSS positioning README テンプレ吸引 + 競合 4 件名指しがカテゴリ 2「並列訴求」構造的該当。**この種のセクション自体が業界平均値**という二重の Gamma 判定を受けて廃案。README は機能説明 + footer "by ぼぶ" 1 行で完結させる（hero「探している答えは、何年か前のあなたが、もう書いている」を維持、L0 vision の「直接書かない」原則に整合）。memory `showhn_launch_benchmarks_2026.md` 「中盤訴求セクション業界テンプレ吸引」事例参照
- [ ] Social Preview 画像 (`assets/og.png`) GitHub repo settings で upload 済み（**user 操作必要**）
- [ ] 15 秒デモ GIF が docs/index.html / README に挿入済み、Vault 名はダミー化済み
- [x] 共通フッター規格（N=1、`bob_persona.md` の規格）の Avatar by Nano Banana Pro 理由付き disclosure が docs/index.html と README 両方に揃っている（2026-05-01 確認: 英版完全一致、日版は意訳「作者: ぼぶ」「8 つのうち 1 つ。」を採用、CLAUDE.md L82 既揃い記録と整合）
- [x] 英文コピーは `humanizer-ja` 翻案チェック済み（スタイロメトリー対策、skill は日本語専用 = 20 パターンを英文に翻案して適用、em dash / 追従的トーン / 太字+コロン / 機能列挙箇条書き 等を機械的に検出 → 2026-05-01 commit `177f3e1` で show-hn-final + reddit 2 媒体に運用実証）
- [x] PyPI（`bobrain 0.1.0`）で `uvx bobrain` が動く最終確認（2026-05-01 確認: `uvx --from bobrain==0.1.0 bobrain --help` 正常応答、4 commands 表示、author=ぼぶ / license=MIT / Homepage URL 整合。pipx は本機未インストールのため未検証、wheel は uvx と同一なので問題なし想定）
- [x] MCP Inspector で MCP プロトコル準拠最終検証（2026-05-01 確認: stdio 経由 initialize → protocolVersion `2024-11-05` 一致 / capabilities 正常宣言、tools/list → `search_docs` 1 個 + inputSchema 整合。⚠️ 軽微: serverInfo.version が FastMCP default `1.27.0` で bobrain 0.1.0 と紐づかない、v0.2.0 改善候補）
- [x] 投稿先別タイトル候補 3 案を準備（HN / r/LocalLLaMA / r/ObsidianMD で訴求軸が違う、後述）

### 開示型の選択（bobrain は Architecture-led + Feature-limited ハイブリッド）

memory `vibe_maintainer_disclosure.md` 参照。bobrain への適用:

- **採用**: 「AI を全能の神」ではなく「特定 architecture boundary（ローカルファースト RAG MCP）に閉じ込めた制御された力」として描く。BrightBean 型の transparency post-mortem 要素も部分採用 OK
- **禁止表現**:
  - 「3 週間で作った」「バイブ・コーディングで爆速」→ 一部には魔法、シニアエンジニアには技術負債赤信号
  - 「全部 Claude Code でやった」→ AI スロップ判定リスク
- **README / hero copy** は体験文（「探している答えは、何年か前のあなたが、もう書いている」）を維持。機能羅列の中盤セクション（「How it performs」「What this is」相当）は **置かない方針確定（2026-05-01）**、v1/v2 両方 Gamma 却下で業界平均値と判定済み（廃案理由は本ファイル「投稿前の最終ゲート」セクション参照）

### 投稿時刻

**月曜 PT 朝（= 日本時間月曜夜 19-21 時）**。投稿後 90 分は Q&A 張り付き必須。火曜も可だが月曜優先。

### 投稿先別の訴求軸

| 媒体 | タイトル軸 | 本文の前置き |
|---|---|---|
| Show HN | 制約 vs 成果（"Show HN: Bobrain – Local RAG MCP for Obsidian + your repos in one query"） | 機能 → install → 1 例 → roadmap、最後に "by ぼぶ" + 1 行 |
| r/LocalLLaMA | ローカル完結 / プライバシー（HN 20pts 超えてから投稿）| 1 段落で「ローカルで動く」価値 + HN URL で「HN で話題」実績強調 |
| r/ObsidianMD | Vault 管理自動化（HN で連携質問発生時に投稿）| Obsidian + code repo 横断検索の体験から入る |

### 投稿後の if-then（撤退 vs 倍プッシュ、定量基準で機械的に）

| 経過時間 | 状態 | アクション |
|---|---|---|
| 30 分 | Points < 2 | **撤退**: 削除 + タイトル修正 + 翌週再投稿検討（front page 浮上絶望、HN ランキング式で復活困難） |
| 30 分 | Points 2-5 | **継続**: コメント返信張り付き、平均 15 分以内に全質問返信。"Thanks!" 短文は順位維持に寄与しない、**技術詳細を語る返信で批判をファンに変える** |
| 1 時間 | Points < 5 | **撤退寄り**: コミュニティ信頼最低ライン未達、削除を検討（コメント率次第で粘る判断もあり） |
| 1 時間 | Points 5-10 | **継続 + r/ObsidianMD 準備**: HN で Vault 連携質問が出たら r/ObsidianMD（Vault 管理自動化軸）に投稿 |
| 1-3 時間 | Points 10-20 | **継続 + r/LocalLLaMA 準備**: front page 入りライン、20pts 超えたら r/LocalLLaMA（ローカル完結軸）投稿準備 |
| 任意 | Points 20+ | **r/LocalLLaMA 倍プッシュ発火**: HN URL を含めて「HN で話題」実績強調 |
| 任意 | front page 入り | **X 倍プッシュ**: 「HN で話題」実績付きで X BuildInPublic 投稿、ハッシュタグは中立、所感は B モードで人格を出す |
| 24 時間後 | front page 残存 | **Lobsters 投稿**（技術詳細軸） |
| 48 時間後 | 安定 | **dev.to 投稿**（チュートリアル形式） |
| 任意 | Comment 率 < 20% | **ボット疑い警戒**: 手動 Penalty リスク、コメントを誘発する返信戦略に切り替え |
| 任意 | `[flagged]` / 灰色表示 | **shadowban 検出**: HN Algolia でドメイン検索 → 新着即時表示確認。別 IP で Newest 順位観察。復旧は hn@ycombinator.com に誠実なメール（Second Chance Pool 掲載依頼可、memory `showhn_launch_benchmarks_2026.md`）|

### Star 獲得層の閾値（投稿後の期待値、撤退判断の参考）

memory `showhn_launch_benchmarks_2026.md` 参照:

- Star 1000+: front page 12h 以上 + 累積 100pts 以上（「圧倒的な効率化」の数値提示が条件）
- Star 500+: front page 6-10h + 50-80pts
- Star 100+: front page 3-5h + 20-40pts
- 二次拡散: 投稿 48h-7d で Awesome リスト / 個人ブログ経由で Star 純増（Context Mode は 228 件純増）

### 撤退判断のメンタル

- bobrain Show HN は **何度でも再投稿できる** 前提（HN ガイドラインで「Second Show HN」許容）
- 30 分 < 2pts で削除しても次週投稿でやり直せる、**撤退コストは低い**
- 1 回目で front page 行かなくても、二次拡散（Awesome リスト掲載）で Star 100 ライン到達は可能
- 削除判断は感情で決めない、**上記定量基準で機械的に**
- 投稿後 90 分の Q&A で疲れて感情判断が出やすいので、**判断は本セクションの表を見ながら行う**

### 投稿後の運用衛生規則（公開後 PR 受付時）

memory `vibe_maintainer_disclosure.md` 参照、bobrain で PR を受け始めたら適用:

- **プロジェクト間汚染防止**: 「bobrain は他プロジェクトを知らない」を維持
- **Zero Framework Cognition**: コアロジックを高レベル FW に依存させない
- **プラグイン優先**: コア追加を避けて integration / extension で対応
- **One concern per PR**: 機械的トリアージのため
- **ドラフト禁止**
- **「エージェントが作ったものはエージェントが直す」**: 数千行の AI 生成 PR を人間が全部読む前提を捨てる

### 鮮度注意

memory `showhn_launch_benchmarks_2026.md` の数値は 2026-04 時点 DR 由来。6 ヶ月で HN コミュニティの空気は変わる。**2026 年 10 月以降に再利用する場合は本判断ロジックの妥当性を再検証**してから適用する。特に「Vibe Coded」受容性は変動の可能性大。

### 関連 memory / ファイル

- memory `showhn_launch_benchmarks_2026.md` — 定量ベンチマーク（撤退ライン / 倍プッシュ閾値 / Star 閾値 / DR 提案 D-7 却下事例）
- memory `vibe_maintainer_disclosure.md` — 開示型 4 分類 + Survival Ratio README 設計レンズ + Vibe Maintainer 衛生規則
- memory `bobrain_pypi_launch.md` — PyPI 公開フェーズ地雷（投稿前段階、token 履歴漏洩 / クリップボード汚染 / PEP 639 等）
- memory `pii_anonymity_recovery.md` — 匿名運用の予防 / 復旧手順
- `.launch-drafts/show-hn-draft.md` v3 — Gamma 通過済み投稿文 draft
- `.agents/director/anti_patterns.md` — bobrain L0 平凡化シグナル 6 カテゴリ
- `docs/research/showhn-strategy-2026-04-29.md` — DR 整形版（Gamma 却下事例の詳細）
- `.launch-drafts/dr-showhn-runtime-ops-2026-05-01.md` — DR「Show HN 戦略的展開」整理（2026-05-01）。Q&A テンプレ 15 件 + 状況別 5 件は bob_persona 矛盾で全採用不可、運用知識（shadowban 6 ステップ / 撤退判断追加 / 90 分タイムライン / 倍プッシュ文体差）を抽出済み

## Dispatch（スマホ）から進める時の境界

Mac 不在中に Dispatch 経由で bobrain を進める場合の可否境界。`dispatch_session_protocol` + `dispatch_skill_compatibility` 準拠。**根拠**: 2026-04-28 stop-trace で `git push origin main` が harness deny されたことから整理。

**進められる**:

- コード編集 / Phase 2 候補（#3 複数ルート / #5 `.bobrainignore` / #6 heading chunking / #7 CoreML）の実装着手
- テスト実行（`uv run python -m pytest -q`、16 cases）
- CLAUDE.md / README.md / docs/index.html 編集 + ローカル動作確認
- GIF 撮影スクリプト準備（`screencapture` + `gifski` のシェルスクリプト雛形）。実撮影は不可
- ローカル commit + log.md 追記（`~/.claude/dispatch-closing-block.md` の正本に従い 1 commit、push しない）
- Show HN / r/LocalLLaMA / r/ObsidianMD 投稿文ドラフト + `humanizer-ja` 通し（インライン展開）
- author rewrite / git-filter-repo 系の準備（実 push は user）

**進められない（user 認可 / GUI / KYC が必要）**:

- `git push origin main` → harness deny（PUBLIC repo default branch 直 push）。User 手動 `! git push origin main` で実行
- PyPI publish（`uv publish`）→ PYPI_API_TOKEN を Dispatch 履歴に流すのは memory `bobrain_pypi_launch.md` の地雷再発。User Mac で `! uv publish --token ...` か事前 keyring 設定で
- GitHub release（`gh release create`）/ Social Preview 画像 upload / repo settings 変更 → ブラウザ GUI
- GIF 実撮影 → macOS GUI + Claude Desktop 実演が必要
- Show HN / Reddit 実投稿 → アカウント認証 + 月曜夜 19-21 時 JST のタイミング合わせ
- NAWABARI / GMO 銀行 / Polar.sh の契約手続（KYC、本人確認動画など）
- Custom skill 実行（`/playable-gate` `/integrate` `/ship-check` 等）→ memory `dispatch_skill_compatibility.md` 通り、Dispatch 受信側では skill が起動しない。**inline で手順を生展開** して Bash/Read/Edit を直接呼ぶことで代替

**運用ヒント**: Dispatch で「PyPI 公開やっといて」「Show HN 投げといて」は不可。「PyPI 公開のための README/CHANGELOG 整備」「Show HN 投稿文 v4 を humanizer-ja 通して `.launch-drafts/` に置いといて」のように **準備系に分解** して投げる。

---

## Phase B 完走（2026-04-30、アプリツリー wiki `log.md` 6 decide エントリ参照）

5 観点診断 + 改造方針確定。**設計禁則 3「罪悪感強要」構造的回避済み**（CLI ツールの応答構造、philosophy-chat の hard constraint 4 件のような対応不要）。bob-survivor と同じ構造的回避パターン。

### Phase B 改造計画（採用要素 4 件追加 + 5 強化、優先順位 1-4）

- 🔲 **要素 9 真実 / 代償の取引 = Pro 版課金**（最優先、重さ補強の物質化）
  - `bobrain init --ide=<claude-code|cursor|claude-desktop>` セットアップウィザード v0.2.0（CLAUDE.md L82 既定）
  - philosophy-chat の 1,200 円課金と同型構造、月額 or 買い切りはマネタイズ wiki 戦略との整合で別途判断
  - anti_patterns カテゴリ 9 逆向き警戒: Pro 版で機能短縮ではなく「ローカルでより便利になる」方向のみ（カテゴリ 3 整合）
- 🔲 **要素 10 キャラのメタ認知 = L1 行為の記憶**（底知れなさ ◎ 達成）
  - Bob が起動回数 / 過去質問パターンを言及（「あなたが昔よく検索したフレーズ」を起動時に表示）
  - 検索結果末尾に「あなたが N 日前にこの言葉で検索しました」を微表示
  - 「不在で語る」原則準拠（meta_cognition_design L33「私はあなたが書かなかった日のことは知らない」推奨）= 監視されている感を出さない
  - anti_patterns カテゴリ 4「便利ツール化」逆向き警戒: L1 演出は「再発見の余地」を強調する文脈で、便利機能としてではない
- ❌ **要素 12 環境ストーリーテリング強化 + 中盤訴求セクション 廃案（2026-05-01）**: v1「How it performs」（実数表型）と v2「What this is, and what it isn't」（境界線型）両方が playable-gate Gamma で却下。**この種のセクション自体が業界平均値**という判定（v1=DR 提案 D-7「実数表型訴求」業界標準テンプレ吸引、v2=OSS positioning README テンプレ + 競合 4 件名指しがカテゴリ 2「並列訴求」構造的該当）。README は機能説明 + footer "by ぼぶ" 1 行で完結、hero copy（L20 体験文）を維持する方針確定。廃案資料は `.launch-drafts/readme-performance-draft.md`（v1）+ `.launch-drafts/readme-performance-draft-v2.md`（v2）として retain。memory `showhn_launch_benchmarks_2026.md` に教訓追記済み
- 🔲 **要素 5 強化 キャラ行動パターン**（既部分実装の細部補強、温度 ◎ 維持）
  - Bob が CLI 出力末尾でサイン的なフッター（無言の演出のみ、anti_patterns カテゴリ 5「ぼぶ人格の侵襲過剰」整合）
  - `bobrain search` の応答末尾に Bob の絵文字 / アスキーアート 1 行など、モード A 維持で滲ませる
- 🔲 **検査経路の運用化**: 改造のたびに `/playable-gate bobrain [--target <変更箇所>]` で L4 関門通す（L0 Taste Layer 既整備、AgentCouncil ループ運用実証あり）

### 不採用 / 適用外要素（Phase B 観点 5 で確定、CLI ツール / RAG サーバーの性質）

- 要素 2 セマンティック・リフレクション: CLI 名 / コマンド名は標準的、改造で追加余地は薄い（自然な命名を破壊するリスク）
- 要素 3, 4, 6, 7, 8: ゲーム要素ではないため適用外
- 要素 11 音響モチーフ: CLI ツール、音響演出文脈外

### 匂い変化予測（Phase A スナップショット → Phase B 改造後）

- 重さ: △ → ◯ （要素 1 強実装 + 要素 9 課金で代償物質化、CLI 性質上 ◎ 達成は困難）
- 底知れなさ: ◯ → ◎ （要素 10 L1 行為の記憶 + 不在で語る演出）
- 温度: ◎ → ◎ （Bob キャラ + 共通フッター規格維持）
- 静謐: 未確定 → ◯ （CLI 出力の余白）
- 不穏: × → △ （L1 行為の記憶で「気配」最小演出）
- 匂い総合: 中（スナップショット）→ **強**（Phase B 改造後）= philosophy-chat と並ぶ匂い ◎ 達成

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
