# Show HN v3 — README/LP positioning aligned (2026-05-19)

**経緯**: v2 (humanized) は user 「価値が出てない」発話で却下。再診断で **post の positioning が README/LP の既存 hero (CLAUDE.md L43 キラーメッセージ「探している答えは、何年か前のあなたが、もう書いている」) と乖離している** ことが判明。v3 は post を README/LP の positioning に揃える。

**README/LP の既 positioning (変更なし、揃える対象)**:
- h1: "The answer you're searching for — you already wrote it, years ago."
- eyebrow: "An MCP server for your Obsidian vault and your Git repos."

**v3 rewrite 軸 (v2 → v3)**:
- 冒頭を「過去の自分が既に答えていた」軸に切り替え (LP hero に対応)
- "AI doesn't know what I already wrote" を more universal な「AI に聞き直してる質問は、過去の自分が既に答えてた」型に拡張
- MCP agent builder 向け段落を 1 つ追加 (audience 拡張: PKM パワーユーザー → AI agent 構築者)
- "Three things" を "Two things" に縮小 (self-help 三点セット軸 3 弱化、memory `gamma_self_check_overreaction`)
- Architecture section を short paragraphs 化、JP-aware を inline ("multilingual RAG that actually handles non-English")
- "Not even error reporting" を独立 1 行 punch
- Title を memory 軸に書き換え

**L0 vision 整合チェック**:
- ✅ 直接書かない (「過去の自分との対話」を直接書かず、概念で滲ませる)
- ✅ Obsidian の高速検索位置付け避ける (memory layer 軸で differentiate)
- ✅ 便利ツール化避ける (具体 query + 3 result で体験を体現)
- ✅ 競合羅列なし (Engraph / obsidian-brain / vaultforge / mcpvault 削除済)

---

## タイトル (v2 から変更)

```
Show HN: bobrain – Local MCP memory of your notes and code, for Claude/Cursor
```

75 chars。v2 「searches my notes and code repos together」は feature-led、v3 は「memory」軸で AI agent 文脈に anchor。HN 黄金時間で MCP タグ trend と整合。

## 本文 (v3)

```
I keep asking my AI coding assistant questions I already answered years ago — in some forgotten Obsidian note, or a README from a long-archived repo. The answer was always already there. It just had no way to surface.

bobrain is a local MCP server that gives Claude / Cursor / Claude Desktop access to those layers. Point it at any directory — your Obsidian vault, ~/code/, anything markdown or source — and it indexes each as a separate namespace. One query hits all of them.

  Q: "How did I think about retry/backoff in any past project?"

  → bobrain returns:
    • a chunk from reliability-notes.md (2023)
    • the actual exponential-backoff implementation from a 2022 repo
    • a related Slack paste in my Obsidian inbox

Under the hood: BM25 + multilingual-e5-large dense, RRF-fused. MeCab Japanese tokenization built in (multilingual RAG that actually handles non-English). Each source becomes a separate namespace — queryable alone or in combination.

Everything runs in-process via ONNX. No telemetry. Not even error reporting.

Two things it deliberately doesn't do:
- Summarize what comes back. You see the raw chunk + file path. When you're trying to find what past-you actually wrote, paraphrase is the enemy.
- Send your data anywhere. The point is your knowledge stays on your disk.

If you're building MCP agents, bobrain is the local memory layer for any markdown or code on disk.

Solo project. Design and tests are mine; commits aren't squashed if you want to read along. Claude Code wrote the implementation under those constraints.

Repo: https://github.com/0916shokichi-blip/bobrain
LP: https://0916shokichi-blip.github.io/bobrain/
Install: pipx install bobrain

Happy to dig into the namespace design, the JP tokenizer choice, or why I picked e5-large over BGE.

— ぼぶ
```

**word count**: 約 370 words。HN sweet spot (300-500)。

---

## v1/v2/v3 進化サマリ

| 軸 | v1 (humanized) | v2 (value surface 1 巡目) | v3 (README/LP aligned) |
|---|---|---|---|
| 冒頭 | "I built bobrain because my notes and my code aren't in the same place" | "Last week I needed to recall how I'd handled a particular OAuth edge case" | "I keep asking my AI coding assistant questions I already answered years ago" |
| 核 punch | なし | "Claude doesn't know what I already wrote" | "The answer was always already there. It just had no way to surface." |
| LP hero echo | なし | なし | あり (「years ago」「already there」が LP hero「already wrote it, years ago」と echo) |
| 競合羅列 | あり (Engraph / obsidian-brain / vaultforge / mcpvault) | なし | なし |
| Example query | なし | あり | あり |
| MCP agent builder 向け | なし | なし | あり ("If you're building MCP agents, bobrain is the local memory layer...") |
| アーキ説明 | 段落丸ごと feature list | 末尾 Q&A 誘導 1 行に圧縮 | 独立段落 + JP-aware を inline punch ("multilingual RAG that actually handles non-English") |
| Privacy line | "no telemetry, no cloud round-trips" 末尾 | 同 | "No telemetry. Not even error reporting." 独立 punch line |
| 「N things doesn't do」 | Three | Three | **Two** (self-help 三点セット軸 3 弱化) |

---

## 投稿前チェックリスト

- [ ] **playable-gate v2 再走 必須** (v2 から positioning 変更で再関門)
- [x] humanizer-ja 風 (textbook 構文 / by design / 形容詞 3 連 等は混入させてない)
- [x] L0 vision 整合 (直接書かない / Obsidian 高速検索回避 / 便利ツール化回避)
- [x] L0 anti_patterns 整合 (思想直書きなし / 平均値スタック言及なし / クラウド侵食なし / 便利ツール化なし / ぼぶ人格侵襲なし / アプリツリー違反なし)
- [ ] og.png upload **未完** (5/20 確認、`open_graph_image_url: null`)。本日 PR #20 で og.png LP/README killer message に同期、merge 後 GitHub Settings/Social-preview に upload 必要 (user 操作)
- [x] PyPI 0.1.0 fresh venv 動作確認 (5/18)
- [x] SECURITY.md 公開 (5/17)
- [x] branch protection 整備済 + drift 修正済 (5/18)
- [x] Dependabot alerts 全 fixed
- [x] PII 流出修正完了 (5/19、本日 filter-repo + force push 経由)
- [x] GitHub Settings: Keep email private + Block CLI push 両方 ON
- [x] README + LP hero positioning と post が一貫
- [ ] demo.gif 撮影 (任意、skip OK)
- [ ] Show HN 投稿実行 (v3 gate 通過後)
- [ ] Reddit drafts (r/LocalLLaMA + r/ObsidianMD) を v3 positioning に更新

---

## Q&A 想定 (v3 用、新規追加分 + v2 から引き継ぎ)

### v2 から引き継ぎ (Q1-Q8)
- Q1: なぜ LangChain ではなく自前実装? → BM25 + fastembed + LanceDB 3 つで sub-second
- Q2: なぜ e5-large over BGE? → 多言語対応 + e5 query/passage prefix が design center と整合
- Q3: なぜ要約しない? → 要約は呼び出し側 LLM 責務、bobrain は chunk + file path のみ
- Q4: code repo 横断はどう違う? → namespace 機能
- Q5: Pro 版は? → 現時点で凍結、OSS 一本で完結 (Show HN ノイズ avoid のため凍結明言は控えるが、Q&A では「OSS 一本予定」程度に答える)
- Q6: Vibe-coded? → 設計・テスト・トレードオフは私、Claude Code は実装担当、commits unsquashed
- Q7: 日本語以外でも動く? → MeCab tokenizer は日本語 path のみ active、英語は標準 BM25 + e5
- Q8: セキュリティは? → SECURITY.md 公開済、二次監査完了、SLA best-effort

### v3 新規 (Q9-Q12)

**Q9: なぜ MCP first? FastAPI とかでも良くない?**
> MCP は Claude / Cursor / Claude Desktop の標準インターフェイスで、Adobe / Sourcegraph / Google も採用検討中。MCP-first にすると、ユーザーが既に使っている AI tool に zero-config で繋がる。FastAPI だとカスタム glue コードを書くか専用 client が必要で、AI agent エコシステム外で孤立する。

**Q10: 「memory layer for AI agents」って具体的に何のこと?**
> あなたが Claude Code skill や Cursor extension、独自 MCP agent を作っているなら、その agent に「あなたのローカルデータの記憶」を持たせる substrate として bobrain を使える。`pipx install bobrain` + `bobrain index <path>` だけで agent から `search_docs` MCP tool 経由で問い合わせ可能。OpenAI Memory / Letta / Mem0 はクラウドベース、bobrain は完全ローカル。

**Q11: ripgrep と何が違う? grep で済むのでは?**
> ripgrep / grep は exact string match。bobrain は semantic similarity (e5 embeddings) + BM25 (語彙重み付き) を RRF で fuse する。例: "retry/backoff" を検索すると、ripgrep は文字列が一致する chunk しか返さないが、bobrain は "exponential delay logic" や "API rate limiting" のような関連表現も拾える。あと ripgrep は file-level、bobrain は chunk-level (paragraph 単位)。両方使い分けで OK。

**Q12: 3-6 sec/chunk は遅くない?**
> CPU での初回 indexing 時の話。検索時は LanceDB の高速 vector index で sub-second。indexing は backgroundで一回走らせるだけ。0.3.0 から hash-aware diff index で 2 回目以降は変更分のみ embed (Phase 2 #12 完了)。Apple Silicon 上で CoreML provider に切り替えれば 5-10x の余地あり (Phase 2 候補)。クラウド embedding API なら速いが、それを使うと「自分のデータを他人の API に預ける」位置付けが崩れる = 意図的に slow CPU を選んでいる。

---

## 投稿後の if-then (memory `showhn_launch_benchmarks_2026` 準拠)

- 30min/2pts 撤退: バックラッシュ avoid、削除しない、1 週間 SNS 止める
- 1h/5pts 信頼線: Q&A 張り付き継続
- 倍プッシュ閾値: front page 残留時間最大化
- 90min 以降: モード A 中立で全質問即答

特別 if-then (v3 新規):
- **「memory layer って大袈裟」攻撃** → Q10 で具体的に answer (「Letta / Mem0 のローカル版」相当)
- **「ripgrep で十分」攻撃** → Q11 で answer (semantic + chunk-level)
- **「multilingual e5 ってどれくらい多言語?」** → 100+ 言語、JP 以外も英中韓独仏西露含む

---

## 並行投稿 (Reddit、v3 positioning に揃え)

- `reddit-localllama.md` を v3 positioning に書き換え (本セッション内で別 file 更新)
- `reddit-obsidianmd.md` を v3 positioning に書き換え

両者は v3 投稿後 24h 以内 or 翌日に投稿、HN 反応見て判断。
