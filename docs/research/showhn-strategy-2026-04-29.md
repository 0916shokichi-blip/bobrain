---
title: Show HN ローンチ戦略（DR 返答整形版）
date: 2026-04-29
source: Gemini Deep Research（プロンプトは /wrap §7 経由で発注）
scope: bobrain v0.1.0 PyPI 公開後の Show HN / Reddit 投稿戦略
status: 参照ドキュメント（実装適用は L4 Playable Gate 経由）
---

# Show HN ローンチ戦略 — 2026 年 4 月時点の実測ベンチマーク

外部 Deep Research で 2025 年 10 月〜2026 年 4 月の Anthropic MCP / RAG / Obsidian 関連 Show HN 投稿 30 件以上を精査した結果。bobrain ローンチ前の判断材料として保存。

## TL;DR

- **2026 の評価軸シフト**: 「AI で作った新規性」→「コンテキスト節約量の実数」。Context Mode の「315KB → 5.4KB」型訴求が支配的
- **生存ライン定量化**: 投稿後 30 分で 2pts 未満 = 撤退候補、1h で 5pts 未満 = 信頼最低ライン未達、comment 率 <20% = ボット疑い扱い
- **倍プッシュ条件**: HN 20pts 超 = r/LocalLLaMA、front page 入り = X、24h 後 = r/ObsidianMD
- **AI 開示の二極化**: 「誠実な全開示」= 受容（Star 100-10000）、「Vibe Coded 強調」= Slop 扱い（Star <50）
- **bobrain 適用上の最大注意**: hero copy への実数導入は L0 anti_patterns（機能羅列）に逆戻りするリスク。**hero は触らず、別セクション「How it performs」を新設して数値を出す** のが安全

---

## 1. 競合 Show HN の実測パフォーマンス

| プロジェクト | 投稿日時 (PT) | 24h pts | front page 滞在 | 最終 Star |
|---|---|---|---|---|
| Context Mode | 2026-02-14 07:15 | 84 | 14 時間 | 9,900 |
| Ctx (/resume) | 2026-04-20 06:45 | 72 | 8 時間 | 112 |
| Agents.json | 2026-03-03 08:30 | 212 | 22 時間 | 不明（高） |
| Open-source Deep Research | 2026-03-03 09:10 | 125 | 16 時間 | 不明（中〜高） |
| Saga (Jira-like MCP) | 2026-02-25 21:43 | 4 | <2 時間 | 20 |
| Need (CLI MCP) | 2026-03-03 07:00 | 4 | <2 時間 | 不明（低） |
| RLM-MCP | 2026-01-15 08:00 | 1 | 圏外 | 3 |
| Treyspace | 2025-11-10 10:20 | 1 | 圏外 | 不明（低） |

### Star 獲得層の閾値

- **Star 1000+**: front page 12h 以上 + 累積 100pts 以上。「圧倒的な効率化」の数値提示が条件
- **Star 500+**: front page 6-10h + 50-80pts。特定モデル（Claude Code 等）への深い機能拡張
- **Star 100+**: front page 3-5h + 20-40pts。ニッチ深掘り（特定言語、特定 IDE）
- **二次拡散**: 投稿 48h-7d で Awesome リストや個人ブログ経由で Star 純増。Context Mode は 228 件純増

---

## 2. 「沈むサイン」の早期検出基準

HN ランキング式 `Score = (P-1) / (T+2)^G`（G=1.8）に基づき、時間経過の減衰を上回る初動が必要。

| 経過時間 | 撤退判断 | 対応 |
|---|---|---|
| 30 分 | Points < 2 | front page 浮上絶望、削除 + タイトル修正 + 翌週再投稿検討 |
| 1 時間 | Points < 5 | コミュニティ信頼最低ライン未達、急速順位低下 |
| 任意 | Comment 率 < 20% | ボット疑いでモデレーターによる手動 Penalty リスク |
| 任意 | `[flagged]` / 灰色表示 | AI slop / SEO スパム通報。`showdead` ON で自投稿確認 |

### Shadowban 検出と復旧

- **検出**: HN Algolia でドメイン検索 → 新着即時表示確認。別 IP で Newest 順位を観察
- **復旧**: hn@ycombinator.com に誠実なメール → Second Chance Pool 掲載依頼可（Anthropic 関連ツールで復活事例あり）

---

## 3. 倍プッシュ媒体戦略

| 媒体 | 優先 | トリガ条件 | 訴求軸 |
|---|---|---|---|
| r/LocalLLaMA | 高 | HN 20pts 超 | ローカル完結 / プライバシー / ハードウェア効率 |
| r/ObsidianMD | 中 | HN で連携質問発生時 | Vault 管理自動化 / ナレッジグラフ影響 |
| X (Twitter) | 高 | front page 入り | 「今 HN で話題の MCP サーバー」実績強調 |
| Lobsters | 低 | 投稿 24h 後 | 技術詳細（Python 実装、FTS5 選定理由） |
| dev.to | 低 | 投稿 48h 後 | チュートリアル形式 / Claude Code 設定ガイド |

### コピーの時間変化

- **24h 以内**: 短期インパクト + 課題解決の直接性 → Upvote 促進
- **48h 以降**: Social Proof（実利用者数） + 長期安定性 → Star（ブックマーク）促進

---

## 4. コメント返信の運用ルール

成功プロジェクト（Ctx, Context Mode）は投稿 12h 以内に **平均 15 分以内** で全質問返信。

- **100% に近い返信率** = HN アルゴリズム上「活発な議論」判定 → 滞在時間延長
- **"Thanks!" 短文返信** は議論を生まないため順位維持に寄与しない
- **技術詳細を語る返信**（例: BM25 ランキング採用理由）が批判的ユーザーをファン化

### 模範応答パターン

**「ChromaDB で良くない？」型 → 差別化軸を即提示**

> ご指摘の通り ChromaDB はベクトル検索で優れています。本サーバーの独自性は「Claude Code のツール呼び出しトークン削減」に特化しており、標準的な RAG よりエージェント推論能力を維持できる設計です。

**「AI が書いたコード」批判 → 設計と実装の分離を明示**

> その懸念は正当です。READMEで開示している通り、設計（Architecture）は人間が担当、実装イテレーションを AI が行いました。MCP Inspector による仕様準拠テストをパスさせています。

---

## 5. 匿名運用 × AI 開示の受容性

### 開示型 4 分類

| タイプ | 事例数 | 受容性 | Star 傾向 |
|---|---|---|---|
| 誠実な全開示（設計者の顔を見せる） | 12 件 | 高 | 100 - 10,000 |
| 「Vibe Coded」強調（責任を AI に転嫁） | 8 件 | 低 | <50 |
| 1 行のみ "Built with Claude" | - | 中 | 「またか」で無視されやすい |
| 1 段落（背景 + ツール選定理由） | - | 高 | 質問誘発、シニア層に届く |
| 専用セクション（プロンプト戦略 + 検証） | - | 高 | 「AI 時代の OSS 開発手法」として注目 |

### 成功の鍵

Context Mode は「Think in Code」というパラダイムを提唱し、AI を「データプロセッサではなくコードジェネレータ」として再定義した。**AI 生成を「手抜き」でなく「新しいエンジニアリングの形」として位置づけたプロジェクトが評価される**。

### 失敗パターン

> 「AI が全部やったのでバグがあるかもしれません」

→ 責任放棄と判定 → 即 flag。

---

## 6. D-7 〜 D-1 アクション（DR 提案、bobrain 適用判断付き）

| Day | アクション | bobrain 適用判断 |
|---|---|---|
| D-7〜D-5 | コンテキスト節約量の実測 + README に表追加 | ⚠️ **hero ではなく別セクション** で。L0 anti_patterns 機能羅立違反回避 |
| D-4 | 「Architected by Human」セクション執筆 | ✅ 採用候補（既存 disclosure draft の補強） |
| D-3 | 否定コメント先回り回答準備 | ✅ ChromaDB / Mem0 / Knowledge-RAG 比較を 3 行ずつ |
| D-2 | PyPI / MCP Inspector で最終仕様準拠検証 | ✅ MCP Inspector は実施推奨 |
| D-1 | 翻訳開示の謙虚な定型文準備 | ✅ 「私は日本人開発者で、この回答は AI 翻訳されています」 |

### 投稿後タイムライン

- **0h (19:00 JST)**: 初コメント投稿（作成動機 / 技術スタック / AI 翻訳の旨）。`pip install` を別端末で再確認
- **1h (20:00)**: Points 5 / Comments 1 を超えているか。showdead で flag 確認
- **6h (01:00 JST 翌)**: front page 入りなら r/LocalLLaMA に「HN で話題」文脈でクロス投稿
- **24h**: Star 50 超なら r/ObsidianMD に「Claude Code ユーザー向け Vault 検索ツール」として
- **72h-7d**: X #MCP / #ClaudeCode エゴサ + 引用 RP。Awesome MCP に PR

---

## 7. bobrain 適用上の判断

### 採用する

- **第 2 章「沈むサイン」基準**: 投稿 30 分後の go/no-go 判断ルールとして即採用
- **第 3 章「倍プッシュ」条件**: HN 20pts 超 = r/LocalLLaMA という閾値はそのまま採用
- **第 4 章「返信運用」**: 投稿後 90 分張り付き（既存ローンチ計画通り）+ 15 分以内返信 + 技術詳細語り
- **第 5 章「開示型」**: 既存 `.launch-drafts/show-hn-final.md` の AI 開示部分を 1 段落以上 + Architecture セクションに補強

### 採用に注意

- **第 1 章「コンテキスト節約量実数」**: bobrain の hero copy（「The answer you're searching for — you already wrote it, years ago.」）は L0 anti_patterns（機能羅列）を意図的に避けた体験文。**実数を hero に持ち込まない**。代わりに README 中盤に "How it performs" セクションを新設して数値提示
- **D-7 実測**: Context Mode 型の「315KB → 5.4KB」相当の節約量計測には、bobrain の場合「Claude Code に context を全文流した時 vs `search_docs` MCP で関連 chunk のみ取得した時」のトークン比較が必要。実測には実 Claude Code セッションが要るので、簡易ベンチ（CLI search で n=5 取得した時の合計 chunk byte）でも初期数値として有用

### 採用しない

- 「Twitter で MCP ハッシュタグ引用 RP」は bobrain の匿名運用（赤ちゃんアバター + 顔出し NG）と整合的に運用できる範囲で。@mention は控えめに

---

## 8. 出典・前提

- 一次ソース: HN Algolia + GitHub Star 推移（DR 側で実測）
- 投稿時間想定: 月曜 PT 朝（= 日本時間月曜夜 19-21 時）
- bobrain 既存準備物: `.launch-drafts/show-hn-final.md`、`.launch-drafts/reddit-localllama.md`、`.launch-drafts/reddit-obsidianmd.md`、`docs/launch/localllama.md`、共通フッター（`bob_persona.md` 規格）

---

_本ドキュメントは DR 返答（Gemini）を bobrain 文脈で整形した参照ノート。原文は会話ログに残存。実装適用は L4 Playable Gate（`/playable-gate bobrain`）経由で個別審査する前提。_
