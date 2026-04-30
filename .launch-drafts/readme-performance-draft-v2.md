# README "What this is, and what it isn't" セクション draft v2

> **❌ 廃案（2026-05-01）**: 本 v2 も playable-gate Gamma で「再起草」判定。OSS positioning README テンプレ吸引 + 競合 4 件名指し（KiwiFS / Stash / ast-outline / your editor's LSP）が anti_patterns カテゴリ 2「既存プロダクトと並べて訴求」構造的該当。v1（実数表型）/ v2（境界線型）の **二重 Gamma 却下 = この種の中盤訴求セクション自体が業界平均値** という判定を受けて、**案 A 採用（README に当該セクションを置かない）**。本ファイルは廃案資料として retain。詳細は bobrain CLAUDE.md「投稿前の最終ゲート」セクション参照。

v1 (`readme-performance-draft.md`) は Gamma 平凡化攻撃で却下（commit `1b890f6`、anti_patterns カテゴリ 4 直撃 + DR 提案 D-7「実数表型訴求」が業界標準テンプレ化）。**Phase B 改造計画 要素 12「環境ストーリーテリング強化 + How it performs 再 draft」=「数値ではなく余白で語る」** 方針で v2 を作成（CLAUDE.md L82 / Phase B 改造計画参照）。

## 配置位置（v1 から変更なし）

`README.md` の `## Roadmap`（L108）直前に挿入。`## MCP client setup`（L76）の後。

## セクション名の変更

- **v1**: `## How it performs`（実数表中心 = カテゴリ 4 直撃）
- **v2**: `## What this is, and what it isn't`（境界線で語る = 競合分析 W18 commit `81fdbb7` の結論を反映）

理由:
- 「How it performs」は機能訴求テンプレ、業界標準で平均値に吸引される
- 「What this is and what it isn't」は **引き受けるもの / 引き受けないもの** の境界で position を語る、stash の 50 行 README に学んだフォーマット
- 数値は背景に置く（誇張ゼロ、必要最小限のみ）、体験を前景に置く

## 採用前提

- `/playable-gate bobrain --target .launch-drafts/readme-performance-draft-v2.md` で 4 段関門通過が **必須**
- Gamma 平凡化攻撃で「数値羅列に滑っていないか」+ 「カテゴリ 4 違反していないか」を確認
- L0 anti_patterns カテゴリ 1（思想表出）/ カテゴリ 4（便利ツール化）/ カテゴリ 5（人格侵襲過剰）の自己チェック必須

---

## draft 本文（v2、要 playable-gate）

```markdown
## What this is, and what it isn't

Bobrain is a **read-only index layer** that sits next to your existing Obsidian vault and your existing git repos. It builds a hybrid BM25 + dense embedding index of your markdown files — Japanese-aware out of the box — and exposes a single MCP tool, `search_docs`, so any MCP-compatible client can search across all of them in one call.

That's the whole shape.

A few things it deliberately is not:

- **Not a virtual filesystem.** Agents don't write through Bobrain. If you want a wiki that AI can edit, look at projects like KiwiFS — they solve a different problem.
- **Not an agent memory consolidator.** Bobrain doesn't summarize your notes into facts, doesn't build a knowledge graph, doesn't run a consolidation pipeline. Stash and similar tools do that. Bobrain returns chunks.
- **Not a code search agent.** If you want AST-aware exploration for code, ast-outline or your editor's LSP will serve you better. Bobrain treats code repos as folders with markdown docs and indexes those.
- **Not a hosted service.** No cloud calls, no telemetry, no account. The index lives in `~/.bobrain/`. The first run downloads a ~2.2 GB ONNX model once; everything after that is your CPU and your disk.

What it is, instead:

- **Japanese-aware by default.** MeCab tokenization is built in. If your vault is in Japanese, you get reasonable BM25 recall on day one — without bolting on a separate tokenizer or shipping it to a cloud service.
- **Multi-namespace.** You can index your Obsidian vault, your active code repo's docs, and a third folder you only touch occasionally, then search across all of them or filter to one. Each namespace is independent — you can rebuild one without touching the others.
- **Aware that your knowledge already lives somewhere.** It indexes the files you already have, where they already are. It doesn't ask you to move anything into a new folder structure.

The use case it was built for:

> *Where did I write about MCP chunking strategies — either in my notes or the code?*

You ask once. Bobrain returns ranked chunks across all your namespaces, cited by file path. You read three of them. One was a Slack-style daydream from eleven months ago that you'd forgotten you wrote. That's the moment the tool exists for.
```

---

## L0 anti_patterns 自己チェック (v2)

**カテゴリ 1（思想表出）**:
- ✅ hero copy に「映す世界」「解釈を変える」を書かない（footer も含めて本セクションには無し）
- ✅ 「過去の自分との再会」を直接訴求せず、最後の段落で **使用シーン** として体験的に置く（"Slack-style daydream from eleven months ago that you'd forgotten you wrote" の語り、ぼぶ口調なし、A モード）
- ✅ 哲学フレーズ直書きなし

**カテゴリ 2（平均値への収束）**:
- ✅ 「LangChain」「OpenAI Embedding」「Notion AI / Obsidian Smart Connections / Mem.ai」のような既存競合並列なし
- ✅ 「全てを記憶する」「無限スケール」「あらゆる」最大化系コピーなし
- ⚠️ KiwiFS / Stash / ast-outline を名指し → **競合直接攻撃ではなく「they solve a different problem」「serve you better」と肯定的に区切る**。これは Gamma 攻撃で「攻撃的でない名指しは平均値か」を要確認

**カテゴリ 3（ローカルファースト侵食）**:
- ✅ 「No cloud calls, no telemetry, no account」明示
- ✅ クラウド連携 / hybrid サービス示唆なし

**カテゴリ 4（便利ツール化）**:
- ✅ 「速い」「軽量」「シンプル」を主張しない（言ってない）
- ✅ 機能比較表 / 数値表ゼロ（v1 で 285× などの数字を全削除）
- ✅ 体験談寄り（"You ask once. Bobrain returns ranked chunks. You read three of them."）= 変容的体験の言語化

**カテゴリ 5（人格侵襲過剰）**:
- ✅ 「俺は」「あんた」なし、A モード中立
- ✅ 赤ちゃんアバター言及なし
- ✅ 思想的リライトなし

**カテゴリ 6（アプリツリー固有）**:
- ✅ Bob 以外のキャラ言及なし
- ✅ Bob を「ぼぶ作者人格」と混同なし
- ✅ bob-universe「沈黙モード」表現流用なし

## v1 からの主要変更点

| 変更点 | v1 | v2 |
|---|---|---|
| セクション名 | "How it performs" | "What this is, and what it isn't" |
| 数値表 | 8 行 + namespace 別 4 行 = 計 12 行の表 | **ゼロ**（"~2.2 GB ONNX model" のみ事実として 1 箇所） |
| 比較対立 | "Stream the whole vault" vs `search_docs` k=5 = 285× reduction | KiwiFS / Stash / ast-outline を **肯定的に区切る**（"different problem" / "serve you better"） |
| 訴求軸 | reduction 倍率の主張 | 引き受けるもの / 引き受けないものの境界 |
| 体験語り | なし（実数のみ） | 最終段落「Slack-style daydream from eleven months ago that you'd forgotten you wrote」で 1 シーン |
| 誇張動詞 | "reduction" | なし（中立記述のみ） |
| 競合言及 | なし（"pathological baseline" は架空敵） | 3 件名指し、ただし「they solve a different problem」と肯定区切り |

## 数値選定の根拠（v2 はほぼゼロ）

- **採用した数値**: `~2.2 GB ONNX model`（事実として 1 回、誇張なし）
- **不採用にした数値**: 285× / 1042 chunks / 456 KB / 333 KB / 1.6 KB / 1.4-2.4 sec/chunk / cold start 15-30 sec
- **不採用の理由**: v1 の Gamma 却下教訓 — 数値が大きいほど誇張感、業界平均値テンプレに吸引される
- **必要時の補助情報**: 数値は別途 `docs/research/measure-context-savings.py` の出力で再現可能、興味あるユーザーが README からスクリプトを辿れる構造で残す

## Gamma 攻撃想定リスク（自己諮問）

playable-gate を通す前に Gamma が攻撃しうるポイントを先回りでリストアップ:

1. **「they solve a different problem」は肯定的に見えて競合宣伝**: KiwiFS / Stash / ast-outline の名前を出すこと自体が広報になる。**反論**: 名指しは「これではない」を明確化する用途で、anti_patterns カテゴリ 4「機能比較表で勝とうとする」の対極（境界線で position を示す = カテゴリ 2 平均値収束を回避する戦略）。memory `external_pattern_evaluation_against_existing_design` 適用 — 競合を名指しで肯定区切りするのは bobrain が意図的に取った position
2. **「Slack-style daydream from eleven months ago」は人格滲ませ過ぎ**: A モード許容範囲か。**反論**: 一人称 / 二人称 / 思想キーワードなし、体験シーンの第三者視点語り。footer での "Made by ぼぶ" は別レイヤーで配置済み（CLAUDE.md L82）。境界線守れている
3. **多言語対応の主張が CJK 一般化**: 「Japanese-aware by default」だけ強調すると他 CJK 言語ユーザー（中国 / 韓国）の印象が悪くなる。**反論**: README なので日本人ターゲットに振って良い、Reddit r/LocalLLaMA / r/ObsidianMD の英語圏ユーザーには Show HN 投稿テンプレで別軸で訴求する設計
4. **"It doesn't ask you to move anything into a new folder structure" は KiwiFS への暗黙攻撃**: KiwiFS が "kiwifs init ./knowledge" で新フォルダを要求する設計を遠回しに批判している印象。**反論**: bobrain の設計選択を述べているだけ、KiwiFS を名指していない（前段の "Not a virtual filesystem" との連続で読むと自然）

## 関連参照

- 競合分析（先行 commit）: `docs/research/competitive-analysis-2026-W18.md`（commit `81fdbb7`）
- v1 廃案資料: `.launch-drafts/readme-performance-draft.md`（commit `1b890f6`）
- L0 director: `.agents/director/anti_patterns.md`
- Memory: `showhn_launch_benchmarks_2026.md` 「DR 提案 D-7 却下事例」
- Memory: `gamma_l0_check.md` 「Gamma 改善案 L0 違反提案チェック」
- 実測再現スクリプト: `docs/research/measure-context-savings.py`（数値情報源として retain）

## 次のアクション

1. このファイルを `/playable-gate bobrain --target .launch-drafts/readme-performance-draft-v2.md` で評価
2. 通過したら README.md に挿入する PR をローカルで作成
3. 通過しなかった場合の Gamma 攻撃論点を本ファイル末尾に追記、v3 を新規作成
