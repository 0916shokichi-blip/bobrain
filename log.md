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
  - `docs/index.html` footer L1108-1117: 既存 bilingual footer のコピーを共通規格に揃える + `.cross-link` CSS 1 ブロック追加
- 暫定 [other tools] リンク先: <https://github.com/0916shokichi-blip>（bob-universe デプロイ前のプレースホルダ運用、bob_persona.md の方針通り）
- 根拠数値: アプリツリー wiki [[2026-04-28-cross-product-branding-richard-ai]] の Richard_ai 事例（Leadmore→Vismore プレセールス $8,400 確保）= 横断ブランド ROI の数値証明
- playable-gate 通過: bob_persona.md で既に規格化されたテンプレ配置のため再評価不要（コピー新規創作ではない）
- 未着手: GIF / Social Preview / Show HN 投稿（人間操作タスク群）

next: Show HN 投稿準備（show-hn-draft.md v3 を user 最終確認 → 月曜夜 19-21 時投稿）
