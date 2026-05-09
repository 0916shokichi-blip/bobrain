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

## [2026-05-01] local | origin push 完了（8 commits、Show HN 投稿前準備の Claude 単独タスク全完了 + N=1 教訓）

**push 結果**: `cb4328a..fbc5fea` = 8 commits 反映、ahead/behind 解消（`## main...origin/main`）。push された内容は Pro 機能設計提案 (v0.2.0) / 競合分析 W18 / 中盤訴求セクション v1+v2 廃案決定 / 投稿前最終ゲート 5 項目検証 / humanizer-ja 翻案 / Show HN 運用 DR 整理 等、Show HN 投稿前段階の作業集積。

**残タスク（user 操作領域、Claude 単独不可）**:

- ⏳ 15 秒デモ GIF 撮影（macOS GUI + Claude Desktop 実演）
- ⏳ Social Preview 画像 (`assets/og.png`) GitHub repo settings から upload（GUI）
- ⏳ 月曜火曜夜 19-21 時 JST に Show HN / r/LocalLLaMA / r/ObsidianMD 実投稿（前段の最終ゲート 5 項目すべてパス済）

**N=1 教訓（user 案内コマンドの cwd 込み記述）**: 本セッション末で push を user に投げる時「`! git push origin main`」とだけ案内したため、cwd `~/` のまま実行されて `'origin' does not appear to be a git repository` エラー。「`! cd ~/projects/bobrain && git push origin main`」と cd 込みで再案内して成功（`cb4328a..fbc5fea`）。**push / commit など cwd 依存コマンドを user に投げる時は `cd <project> && ...` を必ず含める**。再発時に memory 化検討、本回は usage_zero_root_cause 適用で N=1 のみ記録。

next: Show HN 投稿は user 領域、Claude は Q&A 補助 / 投稿後対応に回る（前回 gate `bce2ac4` の next: と一致、push で物理的に到達）

## [2026-05-05] feat | 複数ルート一括 index 実装 (branch feat/multi-root-index)

- **対象**: Phase 2 候補 #3「`bobrain index` 複数ルート一括指定（cold start 15-30 秒）」（CLAUDE.md L46）
- **branch**: `feat/multi-root-index`（main から派生、feat/bobrainignore とは独立。両方 main 凍結維持）
- **仕様**:
  - CLI `bobrain index PATH [PATH ...]` で複数 dir を 1 コールで指定可能
  - 共通 namespace に集約、embedding model の cold start を 1 回に圧縮（M ルート × 15-30s → 1 × 15-30s）
  - 重複ファイルは absolute path で dedupe（`~/notes` と `~/notes/sub` を両方渡しても 1 回処理）
  - 既存 `build_index(root, ...)` API は内部で `build_index_multi([root], ...)` に委譲、後方互換維持
  - watcher は単一 root のまま（責務違うので不変）
- **触ったファイル**:
  - `src/bobrain/indexer.py`: `build_chunks_multi` / `build_index_multi` 追加、既存 `build_chunks` / `build_index` を thin wrapper 化、`Sequence` import
  - `src/bobrain/cli.py`: `paths: list[Path]` positional に変更、`build_index_multi` 呼び出しに切替、出力に `from N root(s)` 追加
  - `tests/test_indexer.py`: +3 cases（複数ルート集約 / 重複ルート dedupe / 空 list 安全）
- **テスト**: `uv run python -m pytest -q` で **19 passed**（既存 16 + 新規 3）。embedding 不要なテスト構造を維持
- **触っていない**: README.md / docs/ / .launch-drafts/ / CLAUDE.md / pyproject.toml（投稿前凍結維持）
- **未対応 (将来)**: namespace 別の複数ルート（現状は全部同一 namespace に集約）/ ルート単位の `--exclude` 個別指定

next: 投稿後 Phase 2 改造再開時に PR / merge 判断（feat/multi-root-index branch retain、push しない）

## [2026-05-05] session wrap | Show HN Q&A 弾薬整備 + 投稿前凍結再確認

**やったこと**:
- `~/Documents/アプリツリー` / `~/Documents/マネタイズ` 未 push 7 件を機密スキャン後 user に push 案内、両 push 完了（私室領域に踏み込まず）
- `~/projects/bobrain/launch/qa-arsenal.md` 新規作成（untracked、12 セクション、投稿当夜の張り付き運用ガイド）
- 投稿テキスト 3 媒体（show-hn-final / reddit-localllama / reddit-obsidianmd）最終再読 → 微調整候補なし判定
- `.launch-drafts/readme-privacy-draft.md` が今日既に整備済を発見（whats-next の 🟡 タスク事実上完了、新規作成回避）

**決定**:
- Q&A 弾薬は「論点 + 核ワード + 禁止表現」で構成、応答テンプレ完成形は書かない（理由: DR が Show HN Q&A テンプレを作ると親切ヘルパーに滑る N=1 教訓 2026-05-01 + bob_persona 整合）
- 投稿テキスト 3 媒体は微調整なしで凍結維持（理由: playable-gate v3 + humanizer-ja 翻案 commit `177f3e1` で既に最適化済、再走は過剰修正で逆に AI ぽくなるリスク）
- `.launch-drafts/readme-privacy-draft.md` は新規作成しない（理由: 別セッションで先回り済、`avoid_duplicate_session_work` 適用）
- `launch/qa-arsenal.md` は untracked のまま維持（理由: whats-next 地雷 #1「投稿前の凍結状態を維持。投稿後に commit」）

**未解決 / punt**:
- src/bobrain/cli.py / indexer.py / tests/test_indexer.py の未 commit 3 件 (94 insertions/8 deletions) を投稿前にどう扱うか — user 判断待ち（commit / stash / 投稿後対応）
- 18:30-19:00 の投稿可否最終確認 — user 領域

**地雷**:
- 🟡 bobrain 未 commit 3 件は私が触らず（別セッション差分、投稿前凍結状態の境界が user 判断で確定）
- 🟡 投稿後 24h の README プライバシー section commit (`readme-privacy-draft.md` 採用) を忘れると Q&A Q3「100% local 本当か」の自己検証誘導が片肺、qa-arsenal.md Q3 と連動済

**次の 1 タスク**: 投稿当夜（5/5 19-21 JST）の張り付き — `launch/qa-arsenal.md` を別ペインで開き、Q&A draft を Dispatch 提示

next: 投稿後 90 分の張り付き完了後に Q&A 実例（実際に来た質問 / 自分の応答）を log.md に追記、qa-arsenal.md v2 整備材料にする

## [2026-05-07] freeze | Show HN 投稿延期 + user 駆動モード移行（期限なし運用）

**事実関係**:
- 5/5 19-21 JST の投稿枠は実施されず（user 申告、5/5-7 で Show HN / r/LocalLLaMA / r/ObsidianMD いずれも未投稿）
- bobrain log.md は 5/5 wrap 以降、本エントリまで沈黙（1.5 日）

**user 状況の前提変更（2026-05-07 user 明示指示）**:
- user は大学 4 年生、水上スキー部、引退 = **2026-09 初週インカレ後**（memory `user_profile_university_waterski`）
- 部活・遠征・大会で作業時間が読めない = 「いつまでに投稿」「次の投稿枠 5/8 火」「窓の終端」のような期限フレームを Claude 側からかけない（memory `feedback_no_deadline_planning`）
- 引退まで user 駆動・時間取れた時に進めるスタイル

**凍結する物**:
- `.launch-drafts/show-hn-final.md` / `reddit-localllama.md` / `reddit-obsidianmd.md` — 投稿テキスト 3 媒体、playable-gate v3 + humanizer-ja 翻案 commit `177f3e1` で最適化済、再走しない（過剰修正で AI ぽくなるリスク）
- `.launch-drafts/readme-privacy-draft.md` — README 統合 commit は user が投稿実施を決めた時に着手
- `launch/qa-arsenal.md` / `.launch-drafts/qa-arsenal.md` — untracked のまま投稿実施まで保持
- `feat/multi-root-index` branch（19 tests pass）+ `feat/bobrainignore` branch — main 凍結維持、PR / merge は user 駆動

**次に bobrain に時間取った時に最初にやること**:
1. `cat ~/projects/bobrain/log.md` で本エントリ確認 + `git log --oneline -10` で差分確認
2. user に投稿実施意思を確認（Claude から「投稿しましょう」と先回り提案しない）
3. 投稿実施が決まったら: README プライバシー section 統合 commit → 投稿テキスト 3 媒体最終再読 → ship-check or playable-gate 再走判断 → user に投稿案内
4. 投稿しない判断なら: Phase 2 候補（#5 `.bobrainignore` / #6 heading chunking / #7 CoreML）の改造に進める選択肢

**未統合の差分（5/5 staged を本 commit に同梱）**:
- 5/5 multi-root-index feat エントリ（branch `feat/multi-root-index`、19 tests pass、main 凍結維持）
- 5/5 session wrap エントリ（投稿前最終ゲート + Q&A 弾薬整備の判断記録）
- 上記 2 件と本「投稿延期」エントリを 1 commit にまとめる（投稿前凍結状態 → 投稿延期 への自然な続き）

next: user が時間取れた時に bobrain 再開。bobrain は凍結状態で待機

## [2026-05-07] correction | 上記 freeze エントリの事実誤認補正（origin/main 進行 + worktree / PR 状況の実態）

**経緯**: 上記 `[2026-05-07] freeze` commit (`8e1e124`、wip/show-hn-freeze-2026-05-05) を打った直後に `git log origin/main` を確認したところ、log に書いた前提が事実と矛盾していることが判明。push してない wip branch なので追記補正。

### 実態（fetch 直後 2026-05-07）

**branch / commit 状況**:
- `origin/main` = `d6d908f feat: multi-root index + .bobrainignore support (#2)` ← **PR #2 merge 済み**
- `origin/main^` = `fb43ade Add CI workflow and list_namespaces MCP tool (#1)` ← **PR #1 merge 済み**
- `local main` = `e7f0c31 docs: Phase C 完了` ← origin/main から見て **ahead 1, behind 2**
- `feat/multi-root-index` = `05c30ac` ← branch 自体は残ってるが内容は origin/main に PR #2 で取り込まれた
- `feat/bobrainignore` = `7161459` ← 同上、origin/main に PR #2 で取り込まれた
- `claude/pdf-chunker` = `0fcc7b4 feat(indexer): PDF チャンカーを追加（pymupdf, ページ単位 + 段落分割）` ← **bobrain log.md / CLAUDE.md に未記録の進行**
- `claude/cranky-darwin-8146e4` / `funny-jackson-29db97` / `wonderful-zhukovsky-f9e984` = Claude Code worktree 3 件、`e7f0c31` (Phase C) 止まり
- `pr2-test-merge` = `deaccc6` Merge `origin/claude/bobrainの-continue-gXnE4: gone`（Claude Code Continue 機能の痕跡）

**freeze エントリの事実誤認**:
- 「`feat/multi-root-index` branch retain、main 凍結維持、PR / merge は user 駆動」 → **誤**: PR #2 で既に origin/main に merge 済み
- 「未対応の Phase 2 候補 #5 `.bobrainignore`」（CLAUDE.md L43） → **誤**: PR #2 で既に origin/main に merge 済み
- CI workflow + list_namespaces MCP tool が PR #1 で追加された事実が **bobrain log.md / CLAUDE.md に未記録**
- PDF チャンカー branch (`claude/pdf-chunker`) も **未記録**

### 何が起きていたか（推定）

- 5/5 以降、Claude Code Continue 機能 / worktree 経由で別経路の作業が進行
- PR #1 / #2 が GitHub Web UI または Continue 機能経由で merge
- bobrain log.md は単一 source of truth として機能せず、別経路の作業が記録されない構造的問題

### user が時間取れた時にやるべきこと（凍結を解く時の手順、期限なし）

1. `git fetch && git log origin/main --oneline -10` で実際の origin/main 状態確認
2. `git log main..origin/main` で behind 2 commits の差分内容確認（PR #1 + PR #2 の実装）
3. `git log origin/main..main` で ahead 1 commit（Phase C 完了 docs）の内容確認
4. 統合判断:
   - (a) `git rebase origin/main` で local main を origin/main にリベース（Phase C docs を後ろに乗せる）
   - (b) `git merge origin/main` でマージ commit 作って統合
   - (c) Phase C docs を捨てて `git reset --hard origin/main` で origin に追従（Phase C docs は別 branch / コピペで取り戻せる場合のみ）
5. CLAUDE.md L37-41「未対応の Phase 2 候補」セクションから #3 multi-root + #5 .bobrainignore を削除（既 merge）→ 残るのは #6 heading chunking + #7 CoreML provider
6. CLAUDE.md「Phase 0/1/3#1/3#2 で完了したもの」セクションに「Phase 2 完了分: multi-root index (PR #2) + .bobrainignore (PR #2) + CI workflow (PR #1) + list_namespaces MCP tool (PR #1)」を追記
7. `claude/pdf-chunker` branch の処遇判断（merge / 廃棄 / 保留）
8. Claude Code worktree 3 件（cranky-darwin / funny-jackson / wonderful-zhukovsky）の処遇判断（残骸ならば削除、用途あれば残す）
9. wip branch `wip/show-hn-freeze-2026-05-05` の処遇判断（本 freeze + correction 2 commit を main に取り込むか、wip のまま放置か）

### 教訓（次セッション起点でも繰り返さない）

- **bobrain 着手前のチェックリスト追加**: `git status --short` + `git branch -vv` + `git log origin/main --oneline -5` を必ず最初に実行（log.md / CLAUDE.md だけ読むのは不十分）
- memory `avoid_duplicate_session_work.md` の典型再発: 「startup hook の whats-next 出力 + log.md 末尾だけ見て判断」で別経路作業を見逃した
- Claude Code Continue 機能 / worktree が動いている repo では、log.md は **単一 source of truth ではない**。GitHub PR / branch / worktree の 3 軸を必ず確認

next: user が時間取れた時に上記「やるべきこと」順で整理。本 correction は wip branch に置いたまま、push しない

## [2026-05-07] check | 投稿実施未確認 → 凍結状態維持

- 親 Claude が「5/5-7 で Show HN / r/LocalLLaMA / r/ObsidianMD 投稿実施したか」を user に確認 → **未実施**
- 上記 `[2026-05-07] correction` エントリの「やるべきこと 9 項目」はそのまま有効、状態凍結維持
- README プライバシー統合 commit (`.launch-drafts/readme-privacy-draft.md` → `README.md`) は **投稿後の KPI 反映前提で punt**（投稿前に統合する場合「100% local」表現が実 vector store / embedding 挙動の裏付けでしか書けず、誇大広告 NG ガード = memory `safe_vibe_coding_checklist` に抵触する可能性）
- 次回再開時必須: `git status --short` + `git branch -vv` + `git log origin/main --oneline -5` の 3 軸 + log.md 末尾 = 4 軸チェック（5/7 correction で確立）

next: user が投稿実施を決断した時点で再開、それまで凍結

## [2026-05-08] sync | CLAUDE.md L44-49 + L294-299 に Phase 2 完了事実反映

`[2026-05-07] correction` の「やるべきこと 9 項目」のうち、**投稿判断と独立に進められる事実整理だけ** を切り出して実施。

### 実施内容

- **CLAUDE.md L44-49 「未対応の Phase 2 候補」**: #3 multi-root + #5 `.bobrainignore` を削除（PR #2 で `origin/main` merge 済 = 2026-05-07）。残= #6 heading chunking + #7 CoreML provider の 2 件
- **CLAUDE.md L294-299 セクション**: 「Phase 0/1/3#1/3#2 で完了したもの」→ **「Phase 0/1/2/3#1/3#2 で完了したもの」** にリネーム + Phase 2 行追加
  - PR #1 (`fb43ade`, merged 2026-05-07): CI workflow (`.github/workflows/ci.yml`) + `list_namespaces` MCP tool 追加
  - PR #2 (`d6d908f`, merged 2026-05-07): multi-root index + `.bobrainignore` サポート追加
- **保持した事実明記**: local main は `e7f0c31` のまま `ahead 1, behind 2`、統合判断（rebase / merge / reset）は user 駆動領域として残す旨を CLAUDE.md に記載

### 手付けず（user 判断領域、9 項目の残）

- 項目 4: local main を origin/main へ統合（rebase / merge / reset の選択）
- 項目 7: `claude/pdf-chunker` branch (`0fcc7b4`) の処遇判断（merge / 廃棄 / 保留）
- 項目 8: Claude Code worktree 3 件（cranky-darwin / funny-jackson / wonderful-zhukovsky）の処遇判断
- 項目 9: wip branch `wip/show-hn-freeze-2026-05-05` の処遇判断（本 sync commit を含めて 3 commit が積まれた状態）

### スコープ理由

- 投稿判断と独立な「事実整理」のみ実施。誇大広告 NG ガード（memory `safe_vibe_coding_checklist`）に触れない
- README プライバシー統合 commit (`readme-privacy-draft.md` → `README.md`) は punt 維持（5/7 check 判断継続）
- untracked `.launch-drafts/qa-arsenal.md` / `launch/` / `readme-privacy-draft.md` は freeze エントリの「投稿実施まで untracked 保持」方針に従い stage しない（memory `git_add_dirty_pickup` 限定 stage）

next: 投稿判断は user 駆動で待機、`origin/main` 取り込み判断も user 駆動。本 sync で CLAUDE.md / log.md 整合性は最低限回復

## [2026-05-09] commune | post-launch ロードマップ第3案 (パターン α 採用)

`/commune bobrain post-launch ロードマップの第3案` を実走 (commune skill N=2)。Codex Augmenter との共創で「Bobrain Lab Notebook」道筋が創発。Phase 0 で既存 Show HN 準備 (10+ commits / playable-gate v3 通過 / humanizer-ja 通し済) を取りこぼしていた errata あり、3 統合パターン (α/β/γ) を提示後 user が **パターン α** (Show HN 予定通り + Notebook + Lab Pass は post-Show HN follow-up) を採用。

### 創発された第3案: 「Bobrain Lab Notebook」道筋 (commune 出力)

bobrain を product ではなく lab notebook として位置づけ直す 4 段 compound 設計:

1. **Notebook 連載 (open)**: `docs/lab/` に月 1-2 本、bob_persona が架空シナリオで dogfood する型を記述、PII 回避は fictional persona シナリオで担保
2. **Lab Pass (closed)**: 「同じ構造を作りたい」発話した読者を $5-10/月で招待、benchmark contributor として匿名 dogfood 結果共有
3. **Phase 2 残機能 (#6 heading chunking + #7 CoreML) を Notebook 駆動で実装**: 機能追加が連載ネタになる compound
4. **Show HN / Reddit はパターン α 採用で予定通り進める** (β「punt」は不採用)

### Codex Phase 3b 検証で追加された制約

各 Notebook 記事で「**検索前の問い → bobrain 検索結果 → 過去ログ再発見 → 同じ構造を作りたい発話**」の 4 段階を **固定フォーマット化必須**。これがないと product-fit 指標 (intent signal) が読後感に流れる。

→ `.launch-drafts/lab-notebook-template-draft.md` に固定フォーマット雛形を作成 (untracked、freeze 維持)。

### Phase 4 残る問い 2 個 → Claude が「任せます」を受けて合理的に決定

- **Q1: Notebook 1 本目の題材** → **「8 アプリ tree (面の 8 つの角度)」** に決定
  - 理由: 構造の再現可能性が最も高い (8 角度 = 即可視化) / 月 1-2 本ペースで連載化しやすい (8 角度 = 自然な目次、半年で 6-8 本) / bob_persona との整合 / PKM パワーユーザーターゲットと整合
- **Q2: Lab Pass 開始タイミング** → **「3 本完走時に Lab Pass 募集開始」** に決定
  - 理由: 3 本で連載として成立 / Polar.sh + KYC + W-8BEN 準備期間 (2-3 ヶ月) を確保 / user 熱量持続限界 / Show HN punt 解除の N=10-30 contributor 目標と整合

### パターン α 採用の理由 (β/γ 不採用)

| パターン | 不採用理由 |
|---|---|
| β: Show HN punt + Notebook 完全方向転換 | 既存 N=10+ commits + DR + playable-gate v3 通過 + humanizer-ja 通しの投資が sunk cost 化、Show HN タイミングを逃す |
| γ: Show HN タイトル / SHOWHN.md に Lab Pass 一段組み込み | Show HN ノイズと Lab Pass intent signal が混ざるリスク + 投稿文の Gamma 通過を再検証する必要 |
| **α: 当初予定 + follow-up** | sunk asset retention / Notebook 連載は post-Show HN なら「Show HN で何が起きたか / どう KPI を読んだか」を最初の題材にできる = bob_persona dogfood に自然な物語性 / Lab Pass の signal 質向上 (Show HN 観客 → KPI 確認 → 「同じ構造を作りたい」濃い intent) |

### 既存ロードマップとの統合 (パターン α)

- **Phase 3 #3 投稿** = **予定通り** (Show HN / r/LocalLLaMA / r/ObsidianMD、CLAUDE.md L189「Show HN 投稿の判断ロジック」セクションをそのまま運用)
- **post-Show HN follow-up** として:
  - Show HN KPI 観察結果が出た直後、Notebook 1 本目「8 アプリ tree 1 角度目」を執筆 (KPI を題材に bob_persona dogfood シナリオを描く)
  - Notebook 3 本完走時に Lab Pass beta 募集開始 (Polar.sh + NAWABARI + GMO 屋号付き口座 + W-8BEN を 2-3 ヶ月で準備)
- **Phase 2 残 (#6 heading chunking + #7 CoreML)** = **Notebook 駆動で実装** (機能追加が連載ネタになる compound、改造のたびに /playable-gate で L4 関門通す既定継続)
- **Phase 3 #4 決済** = **Lab Pass の形で先行実装** (Pro 版本格化は Lab Pass の N=1 検証後)

### 状態 (本 entry 記録時点)

- `.launch-drafts/lab-notebook-template-draft.md` 作成 (untracked、commit せず freeze 維持)
- 本 log.md entry 追加 (unstaged、commit せず freeze 維持)
- CLAUDE.md L43-44 「How to apply」の Phase 3 ロードマップ更新は punt (user が Show HN 投稿実施 + KPI 観察結果が出た時点で反映、freeze 維持と整合)

### next (Show HN 投稿後に踏む)

user が Show HN 投稿実施 → KPI 観察結果が出た直後に:
1. 本 log.md entry を commit (unstaged → staged → commit、wip branch 末尾に積む)
2. `.launch-drafts/lab-notebook-template-draft.md` を `docs/lab/_template.md` 等に昇格して commit
3. Notebook 1 本目「8 アプリ tree 1 角度目」を起草開始 (post-Show HN の物語性を盛り込む)
4. CLAUDE.md L43-44 を更新 (Phase 3 #3 完了 + post-launch follow-up = Notebook + Lab Pass 経路)
