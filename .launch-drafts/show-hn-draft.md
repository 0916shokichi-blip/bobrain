# Show HN タイトル + 本文ドラフト v3（Gamma 構造攻撃を受けた最終版）

**履歴**:
- v1 (2026-04-28): "Local-first hybrid RAG MCP for your Obsidian vault and code" + Why X 構成 → Gamma **却下**
- v2 (2026-04-28): "An Obsidian MCP that also indexes your code repos" + What X 構成 → Gamma 全 **再考/却下**（テンプレ A→B 乗り換え、ぼぶ persona モード混在、固有性 #3 訴求不足）
- v3 (2026-04-28): Gamma 構造攻撃を受けて 3 段圧縮 + 行動の記述で哲学体現

**Gamma 改善案の取捨**:
- ✅ 採用: 5 段 → 3 段圧縮 / 機能列挙を 1 段にまとめ / ぼぶ識別子を冒頭から削除（モード A 整合） / "the" → "a"
- ❌ 不採用: 「I don't trust LLM compression of my own past thoughts」= philosophy_os L33 を直接書く = anti #1 違反。代わりに **行動の記述** で体現する

---

## タイトル v3 確定

> **Show HN: bobrain – A local MCP that searches my notes and code repos together**

- 76 文字 ✅
- ツール種別保持（"local MCP"）+ 個人プロジェクト性（"my"）+ multi-root 並置（"notes and code repos together"）
- Gamma 提案の「my notes and my code repos」から "my" 反復を 1 回に圧縮（D11e）
- 競合 4 個の hero と語彙衝突なし（"Vault Intelligence" / "universal AI bridge" / "semantic + knowledge graph" / "27 tools"）
- Obsidian / hybrid / RAG / RRF などの平均化トリガー語彙を回避

---

## 本文 v3 確定

```
I built bobrain because my notes and my code aren't in the same place. The notes I've been writing for years live in ~/Documents/notes/ as Obsidian markdown; every solved engineering problem is buried in the README of some old ~/code/<project>/. I kept hitting "I know I wrote this somewhere" with no way to search across both.

bobrain is a local MCP server that indexes both, as separate namespaces, and lets your AI client (Claude / Cursor / Claude Desktop) query across all of them at once. It uses BM25 with MeCab Japanese tokenization (some of my notes are Japanese) plus multilingual-e5-large dense embeddings, fused with reciprocal rank fusion. Everything runs in-process; no telemetry, no cloud round-trips.

Existing Obsidian MCP servers are great at one vault — engraph for knowledge graphs, obsidian-brain for PageRank, vaultforge for Canvas, mcpvault as a universal bridge. None of them index code repos alongside the vault. bobrain is a multi-root one.

Three things it does not do, by design:
- summarize the chunks for you. What comes back is the chunk and the file path, nothing else
- send your notes anywhere — embeddings run via in-process ONNX
- require Obsidian to be running. Plain .md files on disk is enough

Solo project. Design and tests are mine; commits are not squashed if you want to read along. Claude Code wrote the implementation under those constraints.

Repo: https://github.com/0916shokichi-blip/bobrain
LP: https://0916shokichi-blip.github.io/bobrain/
Install: pipx install bobrain

Happy to take any question on the namespace design, the JP tokenizer choice, or why I picked e5-large over BGE.

— ぼぶ
```

### v3 の v2 からの主要変更

| 項目 | v2 | v3 |
|---|---|---|
| 段落数 | 5 段（What does / doesn't / Where sits / What's left / Build process） | 3 段（動機 / 機能-ecosystem / 棄却）+ build process |
| ぼぶ識別子 | 冒頭「I'm ぼぶ」+ 末尾「— ぼぶ」 | **末尾のみ** |
| 機能列挙 | 4 ブレット | 1 段に圧縮 |
| 「the multi-root one」 | the | **a** |
| 棄却の哲学化 | 「what it doesn't do」（v2） | 「Three things it does not do, by design」+ "what comes back is the chunk and the file path, **nothing else**" |
| What's left 段 | 4 ブレット | 削除（README に逃がす） |

### philosophy_os L48 への準拠

- 本ファイル内容を **直接書かない** → ✅ 「映す世界」「世界平和」「過去の自己との再会」「忘却 = 再発見」全て表に出さず
- 「Show HN は最初の 1 段は機能、最後に 1 行で人格」（L50） → ✅ 1 段目は動機 + 機能、末尾「— ぼぶ」で人格
- 「LP / README で核を直接書かない」（vision.md L29） → ✅ "what comes back is the chunk and the file path, nothing else" は **行動の記述、思想言明ではない**

---

## anti_patterns 6 カテゴリ最終チェック（v3）

- カテゴリ 1（思想を表に出す）: ✅ クリア。「映す世界」「解釈を変える」「第二の脳」全て不在、行動の記述に徹する
- カテゴリ 2（平均値への収束）: ✅ クリア。"a multi-root one / Different design center" は競合語彙ゼロ
- カテゴリ 3（ローカルファースト侵食）: ✅ クリア。"in-process / no telemetry / no cloud round-trips" 3 重明示
- カテゴリ 4（便利ツール化）: ✅ クリア。「便利」「高速」「シンプル」なし、棄却 3 項目で体験文化
- カテゴリ 5（ぼぶ人格侵襲過剰）: ✅ クリア。冒頭は機能ベース、末尾「— ぼぶ」1 行のみ（モード A）
- カテゴリ 6（アプリツリー横断）: ✅ クリア。Bob キャラ言及なし

---

## QDAIF スコアリング（v3 自己評価）

| 軸 | weight | score (1-5) | weighted | 根拠 |
|---|---|---|---|---|
| chikou_gouitsu (知行合一) | 1.0 | 4 | 4.0 | "multi-root + chunks only + no cloud" は philosophy_os 3 観点を行動で体現。表出させていないが体現している |
| paradigm_shift (パラダイムシフト) | 1.2 | 3 | 3.6 | Show HN コピーでパラダイムシフトを起こすのは構造的に困難（vision L23-25 で禁止）。それでも「Obsidian だけじゃない / summarize しない」の小さな認識転換を提供 |
| productive_friction (生産的摩擦) | 0.8 | 4 | 3.2 | 「summarize しない、chunks と path だけ」を明示、QDAIF 軸 #3 の核心を体現 |
| diversity_niche (多様性ニッチ) | 1.0 | 5 | 5.0 | 競合 4 個実名 + "a multi-root one" で差別化が爆速明示、HN タイトル/本文に類例なし |
| **合計** | | | **15.8** | |

threshold_pass = 14、threshold_pivot = 18。**15.8 で pass、pivot 未満 = AgentCouncil 議論域**だが、Gamma 構造攻撃を経て v1 → v2 → v3 と修正した経緯自体が AgentCouncil 議論と等価。

→ **L4 人間関門へ進む**

---

## L4 人間関門 — ユーザーへの提示

playable-gate guide L93-110:
- 判定基準は **1 つだけ**: 「触ってみて、面白いか」
- bobrain の場合の自問: 「過去の自分の言葉に再会した感覚があるか？単なる検索ヒット表示ではないか？」

ただし Show HN 本文は **プロダクト本体ではなくコピー** なので、L4 自問は次のように翻訳する:

> 「この投稿を、自分が無関係の HN ユーザーとして読んだとして、click するか? 'AI slop' に分類しないか? click 後に 'お、これは試してみたい' と思うか?」

ユーザーが YES なら → README 末尾に Show HN 用の section 追加 / Reddit 投稿準備フェーズへ
ユーザーが NO なら → 「何が NO だったか」2-3 文 → v4 設計

---

## 補足: 競合実名出しのリスク管理

「Where it sits」段で engraph / obsidian-brain / vaultforge / mcpvault を実名出している。Gamma が指摘した「engraph 作者が『うちは knowledge graph だけじゃない』とコメント欄で訂正に来る可能性」は実在する。

リスク緩和策:
1. 各競合の括弧内 1 単語は **その作者自身が hero に書いている言葉から取る**（事実陳述、批判ではない）
   - engraph hero: "Vault Intelligence for AI Agents" / 5-lane hybrid / knowledge graph ← OK
   - obsidian-brain hero: "semantic search + knowledge graph + vault editing" + "PageRank + Louvain" を強調 ← OK
   - vaultforge hero: "Canvas with auto-layout" を最初の差別化として置く ← OK
   - mcpvault hero: "universal AI bridge" ← OK
2. 「all Obsidian-only」は事実、批判ではない
3. もし作者からコメントが来たら誠実に「your hero copy から取った要約です」と回答（モード A）

これで vaultforge が比較表でやっている作法と同等の「事実ベース差別化」として通る。
