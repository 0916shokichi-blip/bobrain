# DR 整理: Show HN における個人開発 AI OSS の戦略的展開

> **保存日**: 2026-05-01 / **ソース**: 外部 Deep Research（提供者: ユーザー）/ **状態**: 既存 CLAUDE.md L82「Show HN 投稿の判断ロジック」への補強候補

## 概要

bobrain 0.1.0 Show HN 投稿前後の運用戦略 DR。HN コミュニティ力学、応答パターン、Q&A テンプレ 15 件 + 状況別 5 件、shadowban 検出、撤退判断、倍プッシュタイミングをカバー。

---

## ⚠️ 採用判定の総括

**Q&A テンプレ 15 件 + 状況別 5 件はほぼ全採用不可** — bob_persona「親切な AI ヘルパーへの退行を回避」と真逆の語り口に滑っているため。

**運用知識部分（shadowban / 撤退判断 / タイムライン / 倍プッシュ文体差）は採用候補** — bob_persona と独立で実用的。

---

## 🔴 不採用部分（業界平均値テンプレ）

### Q&A テンプレ 15 件（全部採用不可）

DR が提示した応答テンプレが ChatGPT 学習データの「親切な OSS メンテナ」中央値:

- Q1: `Great question.`
- Q11: `Absolutely.`
- Q15: `Thank you for catching this.`
- Q3 等: `In our testing, ... provides an exceptional balance...`
- Q7: `We implement a summary-first retrieval pattern similar to jCodeMunch.`

これらは bob_persona「冷淡な哲学者」「人は許すが思想は斬る」と完全に矛盾する。**Show HN 投稿後の Q&A 応答は bob_persona に従って ad hoc に書く** べきで、テンプレート化しない方が安全。

### 状況別 5 パターン応答テンプレ（全部採用不可）

「謙虚さ + 技術的詳細」というありがちなテンプレ。同様に bob_persona と矛盾。

### 競合事例の固有名詞（実在確認できないものは引用しない）

- FlowLens / CostGuardAI / Khoj / TXTOS / Omnara CLI を「成功 / 失敗事例」として引用
- memory `showhn_launch_benchmarks_2026.md` の N=1 事例集には載っていない名前
- DR が捏造したか、または実在しても文脈解釈が誇張されている可能性
- **文中で固有名詞を引用すると裏取りコスト発生 + 誤情報拡散リスク** → 引用しない

### Identity-led 構造の 3 段返信パターン

「妥当性を認め → トレードオフ説明 → 制約を誠実に開示」も業界 OSS テンプレで、bob_persona の「思想を斬る」とは別の語り口。

---

## 🟢 採用候補（CLAUDE.md L82 への補強候補）

### 候補 1: shadowban / flagged 検出フロー — ⭐ 採用

| ステップ | アクション | 判定基準 |
|---|---|---|
| 1 | newest フィードで生存確認 | 投稿後 5 分以内に news.ycombinator.com/newest に表示されない場合 shadowban 疑い |
| 2 | HN Algolia でドメイン検索 | 過去投稿が `[dead]` `[flagged]` になっていないか確認 |
| 3 | フラグ分析 | 「AI-generated design」「wrapper」批判が集中後フラグ → 技術詳細不足が原因 |
| 4 | 誠実な修正 | 「vibe-coded」な外見（紫グラデ、絵文字多用）排除 → プレーンな技術ドキュメント |
| 5 | 公式連絡 | hn@ycombinator.com / 件名: `Show HN: bobrain - Seeking clarification on flagging` / 感情排して知的好奇心を満たす改善点を記述 |
| 6 | Second Chance Pool | モデレーター判断でランダムに front page 下部再掲載、自ら依頼可 |

**統合方針**: bobrain CLAUDE.md L82「Show HN 投稿の判断ロジック」の最後にある「`[flagged]` / 灰色表示」行を本フローで詳細化する候補。memory `showhn_launch_benchmarks_2026.md` への追記も検討。

### 候補 2: 撤退判断追加チェックリスト — ⭐ 採用

既存 30min/2pts ルールに加える観点:

- **コメントの質**: 2pts 未満でも詳細な技術質問が 2 件以上 → 継続（深い興味層に届いている証拠）
- **ネガティブフラグ兆候**: Upvote 増加なのに順位急落 → 複数フラグ可能性、速やかに撤退して内容修正後に数週間後再挑戦
- **競合の同時投稿**: 同様の AI RAG/MCP ツールが front page 既存 → 二番煎じ忌避、その日は撤退

**統合方針**: CLAUDE.md L82 の if-then 表に「コメント質 2 件で深い興味」「Upvote 増 + 順位急落 = フラグ兆候」を追記候補。

### 候補 3: 90 分張り付きタイムラインのフレーム — ⭐ 採用

| 時刻 | アクション |
|---|---|
| T-15min | PyPI 動作再確認 / README 確認 / テンプレ手元 / プロフィールリンク先チェック |
| T+0~30min | newest フィード生存確認 / 15 分おきリロード / 質問 15 分以内返信 / **bob_persona 維持** |
| T+30min | 2pts 以上か判定（既存 CLAUDE.md L82 と整合） |
| T+30~90min | 順位維持 / 批判返信に技術で打ち負かす / 15pts 超えたら r/LocalLLaMA 準備 |

**統合方針**: 既存 CLAUDE.md L82 に時系列が暗黙化されているのを明示化する。

### 候補 4: 倍プッシュの段階文体差 — 採用

| 媒体 | 文体軸 |
|---|---|
| HN | 制約 vs 成果（既存 CLAUDE.md L82 に記載） |
| r/LocalLLaMA | ハードウェア（Apple Silicon, VRAM 使用量）+ ベンチマーク（埋め込み速度） |
| Lobsters | 硬派な技術論（CS 論文寄り、MCP プロトコル設計思想、SQLite 活用法） |
| dev.to | チュートリアル形式（背景 → 技術スタック → 苦労した点、vibe を許容する層へ） |

**統合方針**: CLAUDE.md L82 の「投稿先別の訴求軸」表に Lobsters / dev.to の文体差を追記候補。

---

## 🟡 部分採用候補（要検討）

### 開示型ハイブリッド（Architecture-led + Feature-limited）

memory `vibe_maintainer_disclosure.md` 既存と整合 → 既に CLAUDE.md L82 で「採用」となっている。DR が同じことを言っているだけ、新規価値は無いが既存方針の妥当性確認になる。

### 「3 週間で作った」「全部 Claude Code でやった」を禁止表現とする

memory `vibe_maintainer_disclosure.md` の「Vibe Coded」開示型に既出。新規価値なし。

---

## 重要な N=1 教訓（自己観測）

memory `showhn_launch_benchmarks_2026.md` の警告「DR 提案『実数表型訴求』が業界標準テンプレ化していて Gamma 却下された事例」が **今回も別形態で再発火**:

- 過去（2026-04 DR 提案 D-7）: 「実数表型訴求」が業界平均値
- 今回（2026-05-01 DR）: 「Q&A テンプレ 15 件 + 状況別 5 件」が業界平均値（親切な OSS メンテナ語り口）

**パターン**: DR は「Show HN 用の応答テンプレ」を作らせると親切ヘルパー方向に滑る。bob_persona との直接照合が必須。memory `showhn_launch_benchmarks_2026.md` への追記候補:

> DR を Show HN 応答テンプレ作成に使う時、出力は **必ず親切ヘルパー方向に滑る**。Q&A 完成テンプレを作らせず、運用知識（撤退判断 / shadowban 検出 / 倍プッシュタイミング）の抽出に絞る。

---

## 次のアクション（提案）

1. **CLAUDE.md L82 への追記**: 候補 1（shadowban フロー）+ 候補 2（撤退判断追加観点）+ 候補 3（90 分タイムライン）を統合する PR を提案
2. **memory `showhn_launch_benchmarks_2026.md` 追記**: 「DR は Show HN Q&A テンプレを作ると親切ヘルパー化する」N=1 教訓
3. **本ファイルは廃案ではなく参照資料として retain**（bobrain Show HN 投稿後の Q&A で「言ってはいけないこと」のリストとしても機能する）

---

## 関連参照

- bobrain CLAUDE.md L82 — Show HN 投稿の判断ロジック（既存）
- memory `bob_persona.md` — 発信モード A/B/C 分離、人格テンプレの正本
- memory `showhn_launch_benchmarks_2026.md` — 定量ベンチマーク + DR 平均値吸引の教訓
- memory `vibe_maintainer_disclosure.md` — 開示型 4 分類
- memory `gamma_l0_check.md` — Gamma 改善案 L0 違反提案チェック
- `.agents/director/anti_patterns.md` — bobrain L0 平凡化シグナル 6 カテゴリ
- `.launch-drafts/show-hn-final.md` — Gamma 通過済み投稿文（最終版）
