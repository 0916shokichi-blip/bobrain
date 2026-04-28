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
