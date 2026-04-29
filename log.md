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
