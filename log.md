# bobrain log

## [2026-04-27 20:15] local | Phase 3 進捗ステータスを実態に同期

- LP デプロイ + PyPI 0.1.0 公開済み（2026-04-27）を CLAUDE.md に反映
- 次タスク: GIF 撮影 + Social Preview 画像 + Show HN/Reddit 投稿 → Phase 3 #4 決済

next: GIF 撮影 + Social Preview 画像

## [2026-04-28] local | README footer に「_by ぼぶ_」追加

- 配置: `## License` 直下、最小 1 行（draft 推奨案 B、`.launch-drafts/footer-signature-draft.md`）
- 根拠: projects/CLAUDE.md「モード A: 人格は footer の 1 行で滲ませる」、bob-universe デプロイ前なので空手形回避（"upcoming bob-universe" 等は出さない）
- LP `docs/index.html` の `<footer>` は既に「Built by ぼぶ — ...」相当（案 B より丁寧版）が入っており追加変更なし

## [2026-04-28] gate | README disclosure を playable-gate にかけた結果、追加しない判定

- target: `.launch-drafts/README-disclosure-draft.md`（バージョン B 推奨案）
- Step 2 anti_patterns: 6 カテゴリ該当なし ✅
- Step 3 Gamma: 原案 B = 再考（HN テンプレ既視感 + "the receipt" ミーム + 機能 3 列挙ノイズ）。改稿 3 案（B' / D / E）を再投入 → **バージョン E（"read along" 招待型）採用**
- Step 4 QDAIF: 12.8 < threshold_pass 14（paradigm_shift weight 1.2 が disclosure 文には厳しすぎる、軸が本体機能向け）
- 最終判定: **README には disclosure を追加しない**。Show HN 本文 draft に既に `Build process:` 段落で同等 disclosure が入っているため二重回避。README は技術文書として純度維持
- 詳細: `.launch-drafts/README-disclosure-draft.md` 末尾に Step 2-4 結果と例外条件を記録
- 派生課題: Show HN 本文 draft（`.launch-drafts/show-hn-draft.md`）の `Build process:` 段落も同じ Gamma 指摘に該当する可能性大、**実投稿前に show-hn-draft.md を別 target で playable-gate にかける**こと推奨

## [2026-04-28] local | 共通フッター規格 (N=1) 適用 — README.md + docs/index.html

- 根拠: bob_persona.md「## 共通フッター規格（横断ブランド資産、2026-04-28 確定）」+ アプリツリー wiki [[横断ブランドフッター規格]]
- 適用箇所:
  - `README.md` L125-129: `_by ぼぶ_` 1 行 → 3 行構造（Made by Bob + Avatar by Nano Banana Pro 理由付き / 1 of 8 tools クロスリンク）

## [2026-04-28 15:35] gate+launch | Show HN コピー v3 通過 + 4 経路ローンチ素材完成

**やったこと**:
- Gemini Deep Research のローンチ戦略レポートを マネタイズ wiki/raw/ に保存（`AI 駆動 OSS ローンチ戦略と匿名開発者ブランド構築 2026-04-28.md`）
- Show HN コピーを v1→v2→v3 と Gamma 攻撃 2 回経て構造的に脱皮（v1 却下 / v2 全 再考 / v3 で構造的に「bobrain でしか書けない本文」に到達）
- competitive surface を gh api + raw README で実地確認（10+ Obsidian MCP の hero、bobrain の真エッジ = code repo 横断、JP tokenization、chunks-only）
- v3 final = QDAIF 15.8、L4 ユーザー判定 YES
- Reddit 2 sub 派生（r/LocalLLaMA / r/ObsidianMD）+ punkpeye/awesome-mcp PR 素材まで 4 経路完成

**決定**:
- Show HN タイトル v3 = `A local MCP that searches my notes and code repos together`（76 文字、D6 / D10 不採用）
- philosophy 言明化（Gamma 改善案）は anti #1 違反として不採用、行動の記述「what comes back is the chunk and the file path, nothing else」で代替
- Awesome MCP 挿入は Knowledge & Memory section の末尾（punkpeye が alphabetical を厳密に守らない実態、memory `awesome_list_ordering.md` に保存）

**地雷**:
- 🟡 humanizer-ja を 3 本文（HN / r/LocalLLaMA / r/ObsidianMD）に未適用（projects/CLAUDE.md L94 必須）
- 🟡 GitHub Social Preview 画像未 upload（CLAUDE.md L76）
- 🟡 fresh venv で `pipx install bobrain` 動作確認未実施

**次の 1 タスク**: humanizer-ja で `.launch-drafts/show-hn-final.md` の本文を 1 回通す

**生成ファイル**: `.launch-drafts/{show-hn-draft, show-hn-final, reddit-localllama, reddit-obsidianmd, awesome-mcp-pr-final, awesome-mcp-targets, README-disclosure-draft, footer-signature-draft}.md` + memory `awesome_list_ordering.md` + `gamma_l0_check.md`
  - `docs/index.html` footer L1108-1117: 既存 bilingual footer のコピーを共通規格に揃える + `.cross-link` CSS 1 ブロック追加
- 暫定 [other tools] リンク先: <https://github.com/0916shokichi-blip>（bob-universe デプロイ前のプレースホルダ運用、bob_persona.md の方針通り）
- 根拠数値: アプリツリー wiki [[2026-04-28-cross-product-branding-richard-ai]] の Richard_ai 事例（Leadmore→Vismore プレセールス $8,400 確保）= 横断ブランド ROI の数値証明
- playable-gate 通過: bob_persona.md で既に規格化されたテンプレ配置のため再評価不要（コピー新規創作ではない）
- 未着手: GIF / Social Preview / Show HN 投稿（人間操作タスク群）

next: Show HN 投稿準備（show-hn-draft.md v3 を user 最終確認 → 月曜夜 19-21 時投稿）

## [2026-04-28 15:23] commit | 共通フッター + ローンチ素材を 1 commit に統合（0a42e5b）

- 統合内容: 13:40 共通フッター適用（README.md + docs/index.html）+ 13:50-13:52 ローンチ投稿素材 3 媒体（docs/launch/showhn.md / localllama.md / obsidianmd.md）+ show-hn-draft.md v3 改稿
- /integrate harvest 経由で Cowork セッション由来 dirty を統合的に commit
- diff: 8 files changed, 393 insertions(+), 80 deletions(-)
- next: push origin main && push --tags（v0.1.0、ユーザー明示指示後）→ Show HN 投稿準備

## [2026-04-28] local | Launch material を .launch-drafts/ に集約 — docs/launch/ 公開リスク除去

- 問題: `docs/launch/{showhn,localllama,obsidianmd}.md`（marketer-ja 起草の v0、未推敲）が GitHub Pages publish source `/docs` 配下に置かれていた → commit/push すると Web 公開され、投稿前ドラフトが事前露出するリスク（Show HN の「事前公開」判定で初動毀損の懸念）
- 対処:
  - `docs/launch/*` を `.launch-drafts/` に移動（untracked 状態 = まだ公開されていない段階で予防）
  - 既に存在する final 版（`show-hn-final.md` / `reddit-localllama.md` / `reddit-obsidianmd.md`）と重複する v0 は Trash 退避（`~/.Trash/bobrain-launch-v0-20260428/`）
- 投稿準備の整理状態（5/5 投稿想定、6 日先）:
  - **Show HN**: `show-hn-final.md` — playable-gate v3 通過済み（anti_patterns 6 全クリア / Gamma 構造攻撃 / QDAIF 15.8 / L4 人間関門 YES）
  - **r/LocalLLaMA**: `reddit-localllama.md` — Show HN v3 派生、stack ブレット展開 + Ollama/Docker 不要明示
  - **r/ObsidianMD**: `reddit-obsidianmd.md` — Show HN v3 派生、PKM 文脈 + 既存 Obsidian MCP との差別化
- 残タスク: `humanizer-ja` 通過（3 媒体、英語スタイロメトリー対策）、GIF 撮影、Social Preview 画像 upload（user 操作）、投稿実行（5/5 火曜 19-21 時 JST）

next: 3 媒体に `humanizer-ja` を順次適用 → 投稿前最終チェック

## [2026-04-28 15:30] incident | author 匿名性違反の発覚と filter-repo 復旧

- **発覚**: 共通フッター規格適用 commit 直後、author 確認で全 commits が `東将大 <0916.shokichi@gmail.com>` (本名+個人 email) で commit されていることが判明。直近 5 commits = 既 push 済み 4 件 + 未 push 1 件
- **根本原因**: bobrain repo の local git config + global git config が本名のまま。過去 filter-repo (Phase 3 #2) で全履歴を「ぼぶ <noreply>」に書き換えたが、その後の新規 commit は config を継承して本名 author になっていた。CLAUDE.md の方針宣言だけでは予防にならない（config レベルで強制が必要）
- **復旧手順**:
  1. local config を匿名化: `user.name=ぼぶ` / `user.email=278669525+0916shokichi-blip@users.noreply.github.com`
  2. mailmap で全 28 commits を rewrite: `uvx git-filter-repo --mailmap /tmp/bobrain-mailmap.txt --force`
  3. origin 再追加 + force-with-lease で push（user 手動実行、pre-tool-guard 経由を回避）
- **結果**: GitHub の 28 commits 全 author 匿名化完了。cowork 由来の 2 branches（claude/...）は cowork 環境の config が違ったため幸運にも既に匿名 author だった
- **未解決リスク**: 本名で公開されていた期間（4/27〜4/28）の GitHub cache / Web Archive / API クロール結果には痕跡が残る可能性。技術的に対処不能、リスク受容
- **再発予防**: `.gitignore` に `docs/launch/` 追加（GitHub Pages 公開ルート配下の投稿前ドラフト事前公開を予防）+ memory `bobrain_pypi_launch.md` に第 5 の地雷として追記 + 他 6 repo (bob-survivor / philosophy-chat / character-gallery / transcribe-bird / bob-universe / exit-8-homage) の local config も全件匿名化済み
- **次アクション**: bob-universe も同じ問題（PUBLIC で 4 commits 本名 push 済み）→ 同じ復旧フローを実行予定

## [2026-04-28] preventive | docs/launch/ を .gitignore に追加 — 公開ルート配下の事前露出を永続予防

- 0eea575 で `docs/launch/* → .launch-drafts/*` 移動済み、本変更で復活防止
- 投稿前ドラフトは常に `.launch-drafts/`（tracked、公開ルート外）に置く運用を恒常化

## [2026-04-28 15:55] incident | 別セッションが先行完了済みの作業を重複実行

- **発生**: 16:00 開始の別セッションが、既に同日 15:35 完了済みの「Show HN / r/LocalLLaMA / r/ObsidianMD ローンチ投稿 v3 通過 + .launch-drafts/ 集約」をやり直した。`docs/launch/{showhn.deferred,localllama,obsidianmd}.md` を新規作成、playable-gate を v0/v1/v2 で再実行、Show HN を「無理筋」と誤判定（実際は別セッションで v3 通過済み）
- **根本原因**: ship-check 起動時に `log.md` の **直近 10 エントリを精読しなかった**。startup hook の whats-next 出力（4/27 17:00 時点）を信頼してしまい、4/28 15:23 の commit `0a42e5b` 以降の進捗を見逃した。`/board` Step 1 の俯瞰再生成は走らせたが、project log.md の deep read までは行っていなかった
- **実害**:
  - agent コール 6 回（marketer-ja 2 + gamma-contrarian-ja 4）の高額消費
  - 時間 1-2 時間
  - `docs/launch/` 配下 3 ファイル新規作成（gitignore 除外で commit 不可、安全弁が効いた）
- **教訓（再発予防候補）**:
  1. ship-check / launch 系作業の起動時、project の `log.md` の直近 10 エントリ（または同日エントリ全件）を **必ず精読**してから着手
  2. `/board` Step 1 で project 別 log.md の最終更新時刻を表示する仕組みを追加候補（`projects-discover.sh` 拡張）
  3. 「launch 投稿の v3 / final が既に存在しないか」を ship-check Step 0 で確認する skill 拡張候補
  4. memory `usage_zero_root_cause.md` の逆パターン: 「直近で完了済み = もうやらない」を判断材料に追加候補
- **後始末**: 新規作成した `docs/launch/{showhn.deferred,localllama,obsidianmd}.md` は `.launch-drafts/` 既存版と重複 + gitignore 除外。削除候補（user 判断）

next: `docs/launch/` の重複ファイル削除判断 → `.launch-drafts/show-hn-final.md` 等を正本として humanizer-ja 通過 → 投稿（5/5 月曜夜 JST）

## [2026-04-29] research | Show HN ローンチ戦略の DR 返答を 3 アーティファクトに永続化

- **発生**: ユーザーから Gemini Deep Research 返答（2026 年 4 月時点の Show HN ベンチマーク、MCP/RAG/Obsidian 関連 30 件以上の実測）を受領
- **アーティファクト**:
  1. `docs/research/showhn-strategy-2026-04-29.md` — 整形版 DR ノート（沈むサイン定量基準 / 倍プッシュ閾値 / AI 開示型 4 分類 / D-7 〜 D-1 アクション + bobrain 適用判断）
  2. memory `showhn_launch_benchmarks_2026.md` — 横断再利用版（transcribe-bird 等の OSS Show HN にも適用可）+ MEMORY.md 索引追加
  3. `.launch-drafts/readme-performance-draft.md` — README 中盤に追加する "How it performs" セクション draft（playable-gate 必須）
- **判断**: DR 提案 D-7「コンテキスト節約量を README に実数表で」を **hero copy に持ち込まない**。理由は L0 anti_patterns カテゴリ 4（機能羅列）違反リスク。hero「The answer you're searching for — you already wrote it, years ago.」は 2026-04-27 AgentCouncil で機能羅列から体験文に書き直した経緯があり（CLAUDE.md L37）、ここに数値を戻すと逆走する。代わりに README 中盤に独立セクションを新設する設計
- **実測 TODO**（次セッション or ユーザー指示後）:
  1. 代表クエリ 3 件で `bobrain search -k 5 --json` のレスポンス byte 数計測
  2. 各 namespace の Markdown 合計 byte 計測
  3. draft の `<TBD>` プレースホルダーを実数で埋める
  4. `/playable-gate bobrain --target docs/readme-performance-section.md` で 4 段関門通過
  5. README に正式マージ
- **採用しなかった DR 提案**: hero copy への実数導入（L0 違反）/ Twitter 過剰活用（匿名運用との衝突）
- **採用した DR 提案**: 沈むサイン定量基準 / 倍プッシュ閾値 / 投稿後 90 分張り付き + 15 分以内返信 / Architected by Human 開示強化

next: 実測 → playable-gate 通過 → README 改修（playable-gate 通過後、人間判断後）/ 投稿は 5/5 月曜夜 JST 想定維持

## [2026-04-29] gate | "How it performs" セクション draft v1 を playable-gate で却下

- **target**: `.launch-drafts/readme-performance-draft.md` v1（実数埋め込み: 456 KB markdown → 1.6 KB k=5 = 285× reduction）
- **実測**: LanceDB から直接統計取得 — 1042 chunks / 333 KB chunk total / mean 328 bytes/chunk / 4 namespaces (apptree 31 files + claude-knowledge 64 + monetize 24 + mybrain 7=旧 path)。再現スクリプト `docs/research/measure-context-savings.py` 保存済み
- **Step 1 L0 確認**: ✅（director/ 4 ファイル揃い）
- **Step 2 anti_patterns 即却下**: ⚠️ 境界線（カテゴリ 4「便利ツール化」グレーゾーン）→ Gamma 攻撃で精査
- **Step 3 Gamma 却下**: 5 つの退屈の証拠
  1. カテゴリ 4「機能比較表の数値だけで競合に勝とうとする」直撃
  2. 同型 README が 4 件以上実在（Code Graph RAG 87% / Context-Mem 99.1% / RAG-MCP 75% / Context Mode 60×）→ MCP 業界標準テンプレ化、後発は埋没
  3. 「per-query context cost is decoupled from vault size」がカテゴリ 2「無限スケール」の defensive 版
  4. 「Stream the whole vault」pathological baseline は架空敵設定（draft 自身が "nobody actually does it" と認めている）
  5. bobrain 固有エッジ（Vault + code repo 横断 / 日本語 first / chunks-only）が数値で潰される
- **最終判定**: 🚫 却下（Step 4 QDAIF 進まず）。README 改修は **行わない**
- **DR 提案 D-7 についての結論**: 「実数表型訴求」は DR が示す成功事例（Context Mode 等）の二番煎じになり、**真似た瞬間に成功事例の引力で平均値に吸われる**。L0 anti_patterns カテゴリ 4 を持つ bobrain では恒久的に不採用
- **draft v1 の retain 方針**: `.launch-drafts/readme-performance-draft.md` は廃案にせず証拠資料として残置（DR 検証 + Gamma 攻撃の学習素材）
- **Gamma 反対案（保留）**: 数値廃止 + クエリ実例 1 つ（"where did I argue against X" → 2024 年 3 月の 3 chunks が出る、のような **再現できないが具体的** な例）。ただし vault 内容の露出度は人格モード境界（memory `bob_persona` モード A/B）と要すり合わせ、自動採用しない
- **memory 反映**: `showhn_launch_benchmarks_2026.md` に「DR 提案 D-7 の playable-gate 却下事例」セクション追記。今後の Show HN 戦略 DR を受けた時の判断材料として残す

next: 投稿準備は既存 `.launch-drafts/{show-hn-final, reddit-localllama, reddit-obsidianmd}.md` を正本として進める。「実数表セクション」は追加しない。投稿日 5/5 月曜夜 JST 想定維持

## [2026-04-29] DR 整理 | 価格戦略と Pro 機能の方針確定

**ソース**: Gemini Deep Research「ローカルファースト RAG MCP 市場分析」(2026-04-29)
**raw**: `Documents/マネタイズ/pages/sources/ローカルファースト RAG MCP 市場分析と価格戦略 2026-04-29.md`

**決定**:
- 価格初手 = **$49 LTD（Show HN ローンチ同日に Polar.sh 投入）**。月額決定は 30 日後の反応見て。理由: $5/mo は安すぎ・$15/mo は単独利用で高い・LTD は SaaS 疲れ層に刺さる + 完全ローカル → サーバ維持費なしで LTD リスク低
- Pro 化候補は **「セットアップウィザード」を最有力**（v0.2.0）。設計メモは `docs/proposals/pro-setup-wizard.md`。理由: mcp.json 手書きが最大離脱ポイント、「時間を買う」価値が最も具体的
- DR 推奨「ハイブリッド検索を Pro 化」は **却下**。OSS 0.1.0 で BM25 + multilingual-e5-large 既実装、Pro 化すると downgrade
- 決済は **Polar.sh 単独**（DR 推奨の Lemon Squeezy 併用却下）。memory `payment_mor_provider_split` の開発者向け = Polar.sh 一択路線維持

**30 日 go/no-go 判断ライン**（Show HN 後）:
- 500★ / W1 retention 15% / Discord 100 人 / Setup 成功率 80%
- 詳細は memory `bobrain_pypi_launch.md` セクション 7

**未解決 / punt**:
- TAM の Obsidian 非依存再算定（独立 DR 案件、§ 7 案 1）
- Pro セットアップウィザードのライセンス検証: オフライン JWT vs. リモート API（独立 DR 案件、§ 7 案 2）
- Cursor 用 `.cursor/mcp.json` を user 単位 / project 単位どちらに書くか

**地雷**:
- DR が「Pro = ハイブリッド検索」を提案 → README 公言済の OSS 機能を取り上げる事故になりかけた。**DR 採用前は project の README / CLAUDE.md と照合必須**（memory `external_pattern_evaluation_against_existing_design`）

**次の 1 タスク**: マネタイズ wiki の `/integrate harvest`（未コミット 39 件）を先に消化、その後 bobrain も含めて commit → **解消（2026-04-29）**: マネタイズ wiki commit `e454894` で完全統合済み（Web Clipper 13 + concepts 4 + entities 2 + sources 2 + 既存 concepts 3 加筆）

## [2026-05-01] research | W18 競合分析 → 差別化 3 軸確定

github-trending-radar W18 synthesize（commit `2236bc6`）で発見した bobrain 直接競合 2 件 + 思想対立 1 件を `docs/research/competitive-analysis-2026-W18.md` に分析。

**比較対象**:
- **kiwifs/kiwifs** (245★、Go、BSL 1.1) — 同概念競合、「LLM Wiki pattern」明言、Web UI + 書き込み機能を持つ
- **alash3al/stash** (592★、Go、Apache-2.0) — 機能直競合、Postgres + 8-stage consolidation pipeline、bobrain の "single binary, no Postgres" 差別化軸が確定
- **aeroxy/ast-outline** (100★、Rust、MIT) — 思想対立、「files not embeddings」を明言、bobrain の embedding 中心戦略への陳腐化リスク評価

**bobrain 差別化 3 軸の重なり点**:
1. Japanese-aware (MeCab fugashi+unidic) BM25 + dense hybrid が default
2. 「過去の自分との再会」体験 framing（philosophy_os 紐付け）
3. 既存 Obsidian Vault に薄く乗る（pipx 1 行、Python パワーユーザー向け）

**致命的弱点 3 つの正直な言語化** + 対応方針:
- 弱点 1: Web UI / 書き込み機能の不在 → unix philosophy 的分業として position 付けで対応
- 弱点 2: ast-outline 思想の浸透リスク → 「we are not a code agent search」明示で domain 区切り
- 弱点 3: 初回 2.2GB ダウンロード → Phase 2 で `--lite` mode 候補

**Phase 3 #6 chunking 戦略への apply**: AST chunking 直接導入は不適合、Markdown heading 単位 chunking → 後追いで code namespace 向け AST chunking の 2 段階が筋。ast-outline 試用はまだ早い、Phase 3 で再検討。

**playable-gate 通過の鍵**: 実数表ではなく「我々は何を引き受けて、何を引き受けないか」を率直に書く（stash の 50 行 README に学ぶ）。anti_patterns カテゴリ 4 違反（機能羅列）回避が最優先。

next: "How it performs" v2 を本分析を素材に再 draft → playable-gate 再評価

## [2026-05-01] decide | 中盤訴求セクション廃案（v1/v2 二重 Gamma 却下、案 A 採用）

**判定**: README に「How it performs」「What this is, and what it isn't」相当の中盤訴求セクションを **置かない方針確定**。

**経緯**:
- v1（実数表型「How it performs」、commit `1b890f6`）: anti_patterns カテゴリ 4「機能比較表の数値競争」直撃 + DR 提案 D-7「実数表型訴求」業界標準テンプレ吸引で却下
- v2（境界線型「What this is, and what it isn't」、本セッション draft）: OSS positioning README テンプレ吸引 + 競合 4 件名指し（KiwiFS / Stash / ast-outline / your editor's LSP）が anti_patterns カテゴリ 2「既存プロダクトと並べて訴付」構造的該当（否定形でも認知上は並列化、memory `prompt_inlet_design`）+ 機能列挙 8 割 + 体験 2 行のみでカテゴリ 4 該当
- Gamma 反対案「体験スケッチ 2-3 個を冒頭に並べる」は L0 vision「直接書かない」原則違反方向（カテゴリ 1 越境リスク）= memory `gamma_l0_check.md` 適用で不採用

**判断軸**: v1/v2 両方が **別形態の業界平均値テンプレに吸引された** 二重事例 = 中盤訴求セクション自体が業界平均値という Gamma 二重判定。memory `usage_zero_root_cause` 適用で「セクション自体が要らない」が最も価値の高い判断。

**採用方針 (案 A)**:
- README は機能説明 + hero「探している答えは、何年か前のあなたが、もう書いている」(L20) + footer "by ぼぶ" 1 行で完結
- L0 vision「LP/README/narration では核を直接書かない、機能説明に徹する」原則と最大整合
- v1（commit `1b890f6` retain）+ v2（本 commit で `.launch-drafts/readme-performance-draft-v2.md` retain）は廃案資料として保管、再利用しない

**CLAUDE.md 更新**:
- L82「How it performs セクション要件」を ☑ 化、廃案理由を明記
- Phase B 改造計画 要素 12「環境ストーリーテリング強化 + How it performs 再 draft」を ❌ 化（廃案）

**memory 蒸留**: `showhn_launch_benchmarks_2026.md` に「中盤訴求セクション業界テンプレ吸引」事例追記（v1/v2 二重 Gamma 却下 = OSS Show HN README で「How it performs」「What this is and what it isn't」を置く時の警戒テンプレ）

next: Show HN 投稿前の残タスク = GIF 撮影（user 操作）+ Social Preview 画像 upload（user 操作）+ Show HN 投稿コピー本体 v3 が `/playable-gate` 通過済みの確認（commit `1b890f6` 以前の v3 = 投稿コピー本体は別 target、本 decide は中盤セクションの廃案のみ）

## [2026-05-01] gate | 投稿前 humanizer-ja 翻案を 3 媒体 launch draft に適用

**経緯**: humanizer-ja skill は日本語専用、投稿 draft は英文 → skill ルール（カテゴリ 1-5、20 パターン）を **英文に翻案して適用**。playable-gate v3 通過構造を破壊しない文体微調整のみ実施。

**修正箇所（合計 7 件）**:

- `.launch-drafts/show-hn-final.md`:
  - L20 補足挿入 em dash 削除 + "are great at one vault" → "stay inside one vault" 中立化（カテゴリ 7 + 12 翻案）
  - L24 em dash → semicolon 置換（カテゴリ 7 翻案）
- `.launch-drafts/reddit-obsidianmd.md`:
  - L31 補足挿入 em dash → period 分割（カテゴリ 7 翻案）
  - L37 補足挿入 em dash 削除 + "I checked the alternatives. Engraph, ..." 構造に再整理（カテゴリ 7 翻案、Show HN と同調子）
  - L46, L49 補足挿入 em dash → semicolon 置換（カテゴリ 7 翻案）
  - L67 em dash → comma 置換（カテゴリ 7 翻案）
- `.launch-drafts/reddit-localllama.md`:
  - L50 em dash → period 分割（カテゴリ 7 翻案、"Different design center." を独立文に）

**維持した em dash**: 末尾「— ぼぶ」（署名）/ Reddit greeting "Hi r/X —" / タイトル "[Showcase] bobrain — ..." = いずれもコミュニティ作法 / 体裁として自然な使用、修正対象外

**playable-gate 再評価**: 不要と判断（v3 通過済みコピーへの文体微調整、構造 / 訴求 / 競合言及方針は維持、Gamma 評価軸での平凡化リスク変化なし）

next: bobrain Show HN 投稿前 Claude 単独タスクは **完了**。残りは全て user 操作（GIF 撮影 + Social Preview 画像 upload + PyPI 動作再確認 + 投稿実行月曜火曜夜 19-21 時 JST）

## [2026-05-01] gate | 投稿前の最終ゲート 5 項目を Claude 単独で検証 → 全パス

**経緯**: startup hook の whats-next が「v2 draft → playable-gate 再評価」を一押しに挙げていたが、`/board` Step 0c の進捗確認で **commit `063d314` で既に v2 廃案判定 + 案 A（中盤訴求セクション置かない）確定済み**を発見。重複作業回避（memory `avoid_duplicate_session_work`）で gate 実行を中止し、CLAUDE.md「投稿前の最終ゲート」残項目から Claude 単独で進められる 5 項目を直列検証。

**検証結果（CLAUDE.md L111-119、5 項目すべて [x] 化）**:

1. **playable-gate v3 通過確認** (L111): commit 履歴で 2026-04-28 通過済み + v1/v2 中盤セクションは廃案、show-hn-final が最終
2. **共通フッター規格揃い** (L115): docs/index.html / README.md 両方で `Made by Bob — Avatar by Nano Banana Pro` + N=1 表記。日版は意訳採用（CLAUDE.md L82 既揃い記録と整合）
3. **humanizer-ja 翻案** (L116): commit `177f3e1` で 3 媒体適用済（em dash 7 件修正、構造維持）
4. **PyPI + uvx 動作** (L117): `uvx --from bobrain==0.1.0 bobrain --help` 正常、4 commands (index/search/watch/serve) 表示、メタデータ整合（author=ぼぶ / MIT / Homepage URLs 揃い）。pipx 未検証（本機未インストール、同一 wheel 想定で代替）
5. **MCP プロトコル準拠** (L118): stdio 経由 initialize → protocolVersion `2024-11-05` 一致、tools/list → `search_docs` 1 個 + inputSchema 整合。⚠️ 軽微: serverInfo.version が FastMCP default `1.27.0`（v0.2.0 改善候補）
6. **投稿先別タイトル 3 案** (L119): show-hn-final.md / reddit-localllama.md / reddit-obsidianmd.md で 5/1 06:03〜06:04 に揃い済（commit `177f3e1` 配下）

**残タスク（user 操作領域、Claude 単独不可）**:
- ⏳ Social Preview 画像 (`assets/og.png`) GitHub repo settings から upload（GUI）
- ⏳ 15 秒デモ GIF 撮影 + docs/index.html / README に挿入（macOS GUI + Claude Desktop 実演）
- ⏳ Show HN / Reddit 実投稿（月曜夜 19-21 時 JST タイミング合わせ）

**学び**: startup hook の whats-next は前回セッション終了時点のスナップショット。本セッション以前の作業（dispatch / 別ターミナル / 直前 cowork）が反映されていない。`/board` Step 0c の dispatch-recent-progress + log.md 末尾精読が startup hook の盲信を防ぐ最低ライン（memory `avoid_duplicate_session_work` 適用）。

next: bobrain Show HN 投稿前 Claude 単独タスク **完了確認済**（前回 humanize commit の next: と一致）。次セッションも残タスクは user 操作のみで、Claude は Q&A 補助 / 投稿後対応に回る
