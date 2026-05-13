# director/ 運用規範（横展開資産化、exit-8-homage SOP 由来）

> `philosophy_os.md` / `anti_patterns.md` / `qdaif_axes.yaml` / `vision.md` の 4 ファイルをまたぐメタ規範。bobrain は OSS 公開済 (PUBLIC, MIT) の RAG MCP サーバーで、本 SOP は思想ファイルでなく **実務ガード** として運用する。Codex Augmenter 提案 (commune-loop cycle 9, 2026-05-13)。

## 確立履歴

- **N=0 観察**: bobrain では本 SOP 作成時点で N=2 観察未確立。横展開先での初期化として exit-8-homage の SOP 構造を継承
- **横展開元**: `~/projects/exit-8-homage/.agents/director/_meta.md` (N=2 確立、観点 6 normal 異化 + 観点 7 hommage = 2 階層化パターン)
- **bobrain での N=2 確立予定軸**: 「**ローカルファースト境界**」(成果軸) + 「**手がかり止まり原則**」(成果軸) の positive definition 化候補
- **逆流防止**: exit-8 の N=2 (normal 異化 / 応答率 / hommage) を直接持ち込まない。bobrain 固有の N=2 が立つまで本 SOP の運用は枠組みのみ

## 横断 OS との関係

bobrain `philosophy_os.md` は cross_project_philosophy 継承 + bobrain 固有 3 観点 (**忘却 = 再発見** / **ローカルファースト = 思想** / **検索結果 = 手がかり**) を確立済。本 SOP は新観点を追加せず、**既存 3 観点の更新条件・拒否権・期限管理** を運用する (Codex 提案: 「director/ 追加原則と矛盾させない、新思想を増やすのではなく既存 4 ファイルの更新条件・拒否権・期限管理を書く」)。

## 境界条件の上位性 (bobrain 用置換、N=4 想定)

成果軸 (RAG 検索体験) を理由にして境界条件を押し切ることは禁止。境界条件は常に成果軸より上位。

**境界条件カテゴリ (bobrain 固有)**:

1. **local-first 境界** — データ外部送信禁止 / クラウド同期 / 外部 API 化提案。`philosophy_os.md` 固有観点 2「ローカルファースト = 思想」と同型、Pro 版でも「データを外に出す機能」は最後まで作らない原則と整合
2. **PII ログ境界** — 検索クエリ / index 内容 / user 振る舞いログの収集禁止。`anti_patterns.md` カテゴリ 3 (ローカルファースト思想の侵食) と直結、reviewer #5 redaction layer 実装済みの運用継続
3. **公開 OSS ライセンス境界** — repo MIT 公開済。依存ライブラリ更新時のライセンス分離確認、fork 派生作品出現時に発火 (exit-8 未確定マーキング 8 と同型)
4. **運用持続性境界** — 依存ライブラリ更新 / Python 互換 / PyPI 維持。Phase 3 #4 決済前後で発火可能性 (exit-8 未確定マーキング 9 と同型)

**未確定マーキング (発火 trigger 明示)**:

- 5. **AI 要約化提案** — 検索結果に LLM 要約付与等。固有観点 3「検索結果 = 手がかり」と直接抵触、提案が出た時点で発火
- 6. **外部 API 化提案** — e5-large 推論を OpenAI / Anthropic API に置換等。固有観点 2「ローカルファースト = 思想」と直接抵触、提案が出た時点で発火
- 7. **Show HN / Reddit コピー** — LP / hero / launch post の公開コピー絡みは `/playable-gate bobrain` 必須、README hero copy 改稿時に発火

これら境界条件は「成果軸より上位の拒否権」を持ち、いかに良い RAG 検索体験があっても押し切れない。

## 境界監査手順 (bobrain 用、reviewer 6 項目対処と整合)

director/ では観点 = 内容原則 / 監査 = 運用規範 を分離:

- **匿名性監査**: `git config user.name` / `user.email` が「ぼぶ」匿名固定か確認 (本名漏れ防止、2026-04-28 force push 復旧の教訓、memory `pii_anonymity_recovery` 参照)
- **依存スキャン**: `pyproject.toml` / `requirements.txt` に外部 API 系 (openai / anthropic / google-cloud-* 等) が混入してないか確認
- **クエリログ監査**: `~/.bobrain/` の log / cache / db に PII が残ってないか確認 (reviewer #5 redaction layer 適用範囲外を含む)
- **OSS ライセンス監査**: 新規依存追加時の license compatibility 確認 (MIT 維持)
- **Show HN 直前監査**: README / Social Preview / OG 画像のコピーが `anti_patterns.md` 違反してないか `/playable-gate bobrain --target README.md` 経由

## フロー（exit-8 から継承、bobrain 用調整）

新観点候補 → **Step 1 入口審査** → **Step 2 2 階層化** → **Step 3 連動更新** → **Step 4 分担明示** → **Step 5 評価判定** → **Step 6 閾値期限管理** → **Step 7 Phase 2 実装ガード** → **Step 8 動的閾値発火** (Step 7-8 は bobrain 固有追加)

### Step 1: 入口審査（3 分類、bobrain 用置換）

- **成果軸** (過去の自己との再会 / 忘却 = 再発見 / 検索結果 = 手がかり) → Step 2 へ
- **境界条件** (local-first / PII ログ / OSS ライセンス / 運用持続性 + 未確定 N=5-7) → positive definition 化せず `anti_patterns.md` カテゴリ追加 or `qdaif_axes.yaml` hard_constraint 追加
- **既存観点の下位条件で足りる場合** → 独立観点化せず既存 3 観点に統合 (philosophy_os.md 観点総数維持)

独立観点化の必要条件 (4 つすべて満たすこと、exit-8 同型):
1. 成果指標が既存観点と別に立つ
2. 破壊される価値が既存観点と別に立つ
3. 対応する anti_pattern カテゴリが既存と別に立つ
4. **観測可能な検証文が書ける** (思想で止まらず評価関数として動く)

### Step 2: 2 階層化（成果軸が確定した後）

- 最上位成果指標を **1 つ** に固定
- 下位条件を列挙、**上限 6 個** (6 個超は目録化警告 → 統合 / 削除 / `anti_patterns.md` 退避を検討)
- 並列化禁止 (最上位を支える条件として整理)
- 既存 `anti_patterns.md` (高速検索 / AI 要約 / RAG 化への裏返し) が positive definition 昇格の起点

### Step 3: 連動更新（4 ファイル整合、bobrain 固有）

新観点が成立した時:
- **`vision.md`**: 変容証拠 (ユーザー発話 = 「過去の自分が今の悩みに既に答えていた」等) として検証文を追加 (任意)
- **`anti_patterns.md`**: positive 定義の裏返しとしてカテゴリ補強 or 追加
- **`qdaif_axes.yaml`**: 独立軸追加 or hard_constraint 追加
- **`philosophy_os.md` の `## 関連`**: 横断 OS への接続記述

**接続基準 (形式主義化検出)**: 最上位成果指標は以下のうち **2 つ以上** に接続できること、かつ **片方は `anti_patterns.md` または `qdaif_axes.yaml` 必須**:
- `anti_patterns.md` の対応カテゴリで NG 例が具体化できる
- `qdaif_axes.yaml` examples の high / low で具体例が書ける
- `vision.md` の変容証拠として検証文が書ける

### Step 4: 既存観点との分担明示

- 主担当を 1 観点に固定
- 参照する既存観点 **1-2 個** までに制限
- 二重加点禁止記述は **1 行** (N=10 でも管理可能)

### Step 5: 評価判定の 3 段階化

「弱 / 中 / 最高位（成果指標達成）」の達成度基準を観点末尾に明示。

### Step 6: 閾値期限管理（暫定据え置きの長期化警戒）

新軸追加 / hard_constraint 追加で `qdaif_axes.yaml` の `threshold_pass` / `threshold_pivot` を暫定据え置きにする場合、**N+1 サイクル以内に再計算** を Phase 4 残る問いに固定。

### Step 7 (bobrain 固有): Phase 2 実装ガード

Phase 2 候補 #6/#7/#8 実装提案が出た時点で本 SOP が機能ガードとして発火:

- **#6 Markdown heading 単位 chunking**: `anti_patterns.md`「平均値への収束」発火確認 (LangChain ベース / OpenAI Embedding への降格でないか)
- **#7 CoreML provider 化**: 外部 API 化提案でないこと確認 (local-first 境界 1 / 固有観点 2 に整合)
- **#8 auto-sops/ + Reflection scheduler hook**: 「過去の自己との再会」観点と整合確認、PII ログ境界 2 確認、`vision.md` 「自己と過去の自己との対話」と方向一致確認 (Photo-agents L3/L4 移植、memory `agent_memory_layer_architecture` 参照)

### Step 8 (bobrain 固有): 動的閾値発火（Codex 提案、cycle 9）

QDAIF score の `threshold_pivot` だけでなく、以下を **hard trigger** とする:

- **外部 API 化提案** が出た cycle
- **自動要約化提案** が出た cycle
- **PII ログ収集案** が出た cycle
- **クラウド同期案** が出た cycle

これらは `qdaif_axes.yaml` の threshold_pivot 即発火、director/ 議論を強制再開。Show HN 投稿前 / Phase 3 #4 決済前後 / Pro 版機能設計時の 3 タイミングで運用ガード。

## 観点総数の上限（exit-8 と同型継承）

- **soft cap 10 / hard cap 12 / 観点 11 以降は統合レビュー必須**
- 現状 bobrain は固有 3 観点 (忘却 = 再発見 / ローカルファースト = 思想 / 検索結果 = 手がかり)、追加余地大だが新規追加より既存 3 観点の更新条件・拒否権運用を優先 (Phase C 補強 1「director/ 追加は原則停止」と整合)

## SOP の横展開元・自己制約

- **横展開元**: `~/projects/exit-8-homage/.agents/director/_meta.md` (N=2 確立、commune-loop cycle 3 抽出)
- **N=2 観察予定軸**: bobrain は 「ローカルファースト境界」+「手がかり止まり原則」で N=2 を立てる方針 (Codex 提案、cycle 9)
- **本 SOP は N=0 観察ベース**、N=2 確立後に再評価必須
- **bobrain 固有の anti-pattern** (「外部 API 化を選択肢として残す」「LLM 要約付与を MVP に含める」等) が出たら、Step 1 入口審査で即却下する経路を確認
- **横展開資産化の証跡**: 本 SOP を「exit-8 from bobrain」と分離可能な形で運用 (cycle 9 ledger 記録 + 各 project 固有部分は個別)

## 関連

- `philosophy_os.md` 固有観点 1-3 (横断 OS 継承 + bobrain 固有 3 観点)
- `anti_patterns.md` 既存 3 カテゴリ (思想を表に出す / 平均値収束 / ローカルファースト侵食)
- `qdaif_axes.yaml` 既存 4 軸 (chikou_gouitsu / paradigm_shift / 他 2 軸)
- `vision.md` 変容証拠 (過去の自己との対話、忘却 = 再発見の余地)
- **横展開元**: `~/projects/exit-8-homage/.agents/director/_meta.md`
- **確立 cycle**: `~/.claude/commune-loop-ledger.md` exit8-1 cycle 1-3 (元 SOP 抽出) + exit8-3 cycle 9 (本 SOP 移植開始)
- **横展開ルール**: `~/projects/exit-8-homage/.agents/director/_meta.md` 「SOP 横展開資産化」セクション
- **関連 memory**: `pii_anonymity_recovery` (匿名性監査) / `agent_memory_layer_architecture` (Phase 2 #8 auto-sops) / `safe_vibe_coding_checklist` (Show HN 直前監査)
