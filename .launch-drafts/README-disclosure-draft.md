# README disclosure ドラフト（playable-gate 通過前の素材）

**目的**: README に AI 駆動開発である事実を「アーキテクチャ主導 / Claude が実装担当」のスタンスで開示する。projects/CLAUDE.md の「モード A: 中立・機能ドリブン」「人格は footer の 1 行で滲ませる」と整合。

**根拠**:
- `Documents/マネタイズ/raw/AI 駆動 OSS ローンチ戦略と匿名開発者ブランド構築 2026-04-28.md` の「成功したディスクロージャーの言い回し」表「アーキテクチャ主導」カテゴリ
- 失敗パターン回避: 「Vibe-coded」と開き直る / LLM くさい README フォーマット（過度な太字・誇張）

**配置候補**:
- (a) `## License` の手前、新セクション `## How this was built`
- (b) `## What it is` の直後（ヒーロー文の信頼補強として早めに置く）
- (c) `## License` の直後、最終行に footer 形式で置く

---

## バージョン A — 最小（1 sentence）

> **About the build**: I designed the architecture, the tradeoffs, and the test suite; Claude Code wrote the implementation. Commits are unsquashed if you want to see the trail. — ぼぶ

- **狙い**: HN の hacker 層に「ガバナンスは人間側」と即伝える。コメント欄での技術的質問に弾薬を残す（タグライン代わり）
- **長さ**: README に 2-3 行
- **リスク**: 短すぎて「具体的に何を AI に書かせたのか」の追加質問を必ず受ける（→ 利点でもある、Q&A の入り口になる）

## バージョン B — 中（リサーチ推奨に近い）

> **How this was built**: I designed the architecture, made the tradeoff calls — local-only by default, BM25 + e5 hybrid retrieval, Japanese tokenization in the default install — and own the test suite. Claude Code wrote the implementation under those constraints. The unsquashed commit history is the receipt. — ぼぶ

- **狙い**: 設計判断の中身（local-only / hybrid / 日本語）を 1 文に畳むことで、「AI に丸投げではない」ことを実証する
- **長さ**: README に 4-5 行
- **リスク**: 機能羅列にも読める → anti_patterns カテゴリ 4（機能羅列型）に抵触しないか playable-gate で要評価

## バージョン C — 長め（思想を一段滲ませる、モード A 限界）

> **Build process**: One person (ぼぶ) directing Claude Code as the implementation pair. I made the design calls — local-only by default, hybrid retrieval, Japanese tokenization out of the box — and Claude wrote the code under those constraints. The reason the constraints look the way they do is that I don't want my notes leaving my machine; that's the whole point of the project, not a feature. — ぼぶ

- **狙い**: 「local-only は機能ではなくプロジェクトの本旨」を一行で示し、思想モード B に踏み込む手前で止める
- **長さ**: README に 6-7 行
- **リスク**:
  - 「the whole point of the project, not a feature」は projects/CLAUDE.md 的にはモード A 寄りの限界点
  - 「映す世界を間違えた」「世界平和」「裏側の駆動力」は **絶対に表に出さない**（cross_project_philosophy 規範）。本ドラフトもそこは守っている
  - playable-gate の anti_patterns カテゴリ 1（思想の出しすぎ）に触れないか要評価

---

## 推奨

**バージョン B + 配置 (a)** を一次案として playable-gate に投入。

理由:
- A は短すぎて差別化に欠ける
- C は projects/CLAUDE.md の「モード A は 1 行で滲ませる」原則の上限ぎりぎり
- B は具体性 + 抑制のバランスが取れており、HN コメント欄での Q&A に展開しやすい

**playable-gate 起動コマンド**:
```bash
/playable-gate bobrain --target .launch-drafts/README-disclosure-draft.md
```

通過したらバージョンを 1 つ選択して README.md に反映。

---

## 2026-04-28 playable-gate 実走結果: 🚫 README には追加せず

`/playable-gate bobrain --target .launch-drafts/README-disclosure-draft.md` 実走。

### Step 2: anti_patterns 6 カテゴリ ✅ 該当なし

### Step 3: Gamma 平凡化攻撃

- バージョン B（原案）: **再考**。「I designed X → Claude wrote Y → receipt」は HN 2025-2026 の AI 駆動 OSS disclosure テンプレ。"the receipt" は X / HN 2024+ で消費し尽くされたミーム。機能 3 列挙が disclosure の本旨を薄める
- バージョン B'（語順組み替え版）: **条件付き採用**。構造同一でテンプレ既視感残存
- バージョン D（短縮型）: **却下**。「Solo project.」「Commits unsquashed.」は HN defaults of defaults
- バージョン E（招待型 "if you want to read along"）: **採用**。「verify」「receipt」系の検証フレームを捨てて「読み物として並走」の能動的招待に置き換えた点が識別性

採用候補テキスト（バージョン E）:
```
## How this was built

Solo, with Claude Code as implementation pair. Design decisions, tradeoffs, and tests are mine; commits are not squashed if you want to read along. — ぼぶ
```

### Step 4: QDAIF スコア

- chikou_gouitsu (×1.0): 4 — 思想を表に出さず、ガバナンス可視化に徹し言行一致
- paradigm_shift (×1.2): 2 — disclosure 単独でユーザー認識転換は起こせない、限定的
- productive_friction (×0.8): 3 — read along は軽い能動性要求、本体精神と整合
- diversity_niche (×1.0): 4 — テンプレから抜けたと Gamma 認定

**合計 12.8 < threshold_pass 14 → 却下範囲**

### 最終判定: README には disclosure を追加しない

理由:
1. QDAIF 12.8 で threshold 未達
2. **Show HN 本文 draft の `Build process:` 段落に同等の disclosure が既に入っている**（`.launch-drafts/show-hn-draft.md` の本文 4 段落目）→ README に新セクションを足すと **二重** になる
3. README は技術文書として純度を保ったほうが、機能優先の hacker 層に親和性が高い
4. footer 「_by ぼぶ_」（README 末尾、2026-04-28 commit be85293 で追加済み）で「個人作 + 人格を 1 行滲ませる」は最小ルートで賄えている

### Show HN 本文側の課題

`.launch-drafts/show-hn-draft.md` の `Build process:` 段落も同じ Gamma 指摘（テンプレ既視感 / "the trail" = receipt 系装飾）に該当する可能性大。**実投稿前に Show HN 本文を別途 playable-gate にかけるべき**（target を show-hn-draft.md にして再実行）。バージョン E の「commits are not squashed if you want to read along」表現を本文に流用する選択肢もあり。

### この判定の例外条件（再評価のトリガー）

以下のいずれかが起きたら README disclosure 追加を再検討:

- Show HN 投稿後、コメント欄で「Vibe-coded」「AI slop」と分類されて反論用テキストが必要になった
- README 単独で repo を発見した訪問者から「誰が作ったのか / どう作ったのか」の Issue / Discussion が立った
- bob-universe デプロイ後に footer 形式が変わる（"part of the upcoming bob-universe" 等の連続性訴求）
