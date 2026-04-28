# Show HN タイトル + 本文ドラフト（playable-gate 通過前の素材）

**目的**: Show HN 投稿用のタイトル候補と本文ドラフト。playable-gate に投入してから決定する。

**根拠**:
- リサーチ raw: `Documents/マネタイズ/raw/AI 駆動 OSS ローンチ戦略と匿名開発者ブランド構築 2026-04-28.md`「投稿タイトルの成功・失敗パターン」「【投稿日】Local-first / Privacy を前面に」
- bobrain CLAUDE.md キラーメッセージ「探している答えは、何年か前のあなたが、もう書いている」
- 既存 README L4 ヒーロー: "The answer you're searching for — you already wrote it, years ago."

**HN タイトル制約**: 80 文字を超えると `(...)` で truncate されることが多い。可能なら 80 以内、最大 90 まで。

---

## タイトル候補（4 案、各長さチェック付き）

### A. リサーチ忠実型（既存エコシステム補完を強調）
> Show HN: bobrain – Local RAG MCP for Obsidian and your code repos (zero-cloud)

- **長さ**: 78 文字 ✅
- **狙い**: HN 層に「local-first / zero-cloud」を 2 単語で刺す
- **弱み**: AI 開発開示が title にない（→ 本文 1 行目で補う）
- **anti_patterns チェック**: 機能羅列ではない、誇張なし

### B. 「1 人 + AI」型（HN の hacker 精神に直撃）
> Show HN: bobrain – I built a local MCP RAG for my Obsidian + repos with Claude Code

- **長さ**: 86 文字（やや長い）
- **狙い**: 「1 人で構築 + ターゲット明示」の HN 黄金パターン
- **弱み**: タイトルに AI 開発が出ているので「AI slop」に分類されるリスク（→ disclosure 文の質次第）
- **anti_patterns チェック**: 「revolutionary」「ultimate」のような形容詞なし、具体的

### C. キラーメッセージ型（thoughtful 路線）
> Show HN: bobrain – The answer you're searching for, you already wrote years ago

- **長さ**: 80 文字 ✅
- **狙い**: 既存ヒーロー文と一致、単発のツールではなく「体験」を売る
- **弱み**: HN は機能を見たい層が多い → これだけだと「何のツールか」が分からず click 損失の可能性
- **anti_patterns チェック**: 体験文で機能羅列ではない、しかし「解釈を変える」を漏らしてないか要評価

### D. 二段ハイブリッド（推奨）
> Show HN: bobrain – Local-first hybrid RAG MCP for your Obsidian vault and code

- **長さ**: 79 文字 ✅
- **狙い**: 「Local-first / hybrid / MCP / 対象（Obsidian + code）」を 1 行に圧縮、AI 開発開示は本文最初の段落で
- **弱み**: hybrid という単語が読者に伝わるか（BM25 + dense の説明は本文で）
- **anti_patterns チェック**: 機能寄りだがそれは HN の作法、誇張なし

---

## 推奨

**タイトル D + 本文（後述）** を一次案として playable-gate に投入。

理由:
- A は無難だが「hybrid」を落とすと bobrain の差別化（多くの local RAG が dense 単独 or BM25 単独）が見えない
- B はタイトルに「AI で作った」が出る。本文でディスクロージャーする現代的な作法と二重になる
- C は思想モード B 寄り、Show HN という場と相性が悪い
- D が Local-first / hybrid / MCP / 対象 の 4 要素を 80 文字以内で全部入る最良圧縮

---

## 本文ドラフト（v1）

```
Hi HN — I'm ぼぶ. bobrain is a local-first hybrid RAG MCP server I built so my AI client (Claude / Cursor / Claude Desktop) can search my Obsidian vault and my code repos in a single query.

Why hybrid: BM25 catches the exact filename or term you half-remember; e5 (multilingual-e5-large via fastembed/ONNX, fully local) catches the meaning when you've forgotten the words. The two are fused with reciprocal rank fusion. Japanese-aware out of the box (MeCab via fugashi + unidic-lite).

Why local: I don't want my notes leaving my machine. Embeddings run in-process. There's no cloud component. The first index pulls the e5 weights (~2.2 GB) into the fastembed cache; after that everything stays on disk.

Why multi-root: my brain isn't in one folder. It's split across an Obsidian vault and the README/docs of every active repo. bobrain indexes them as separate namespaces and lets you query across all of them at once.

Build process: I designed the architecture, the tradeoffs, and own the test suite. Claude Code wrote the implementation under those constraints. Commit history is unsquashed if you want to see the trail.

Repo: https://github.com/0916shokichi-blip/bobrain
LP: https://0916shokichi-blip.github.io/bobrain/
PyPI: pip install / pipx install bobrain (Python 3.12+)

Roadmap: PDF chunking via pymupdf, heading-aware Markdown chunking, code-AST chunking via tree-sitter, optional reranker. Today it's Markdown-only.

Happy to take any question on the design — especially around the JP tokenizer choice and why e5-large over BGE.
```

**長さ**: 約 1500 文字（HN は本文長さ制限なし、長すぎても OK だが 1000-2000 字が一般的）

**狙い**:
1. 1 段落目: 何のツールか / 誰向けか
2. 2-4 段落目: 「Why X」を 3 つで設計判断を即座に開示（→ HN の質問先回り）
3. 「Build process」段: README disclosure と同じスタンスで AI 開発を開示（B/D タイトル選択時はここが必須）
4. リンクは GitHub / LP / PyPI を明示
5. 締めの「Happy to take any question on」で Q&A を誘発（HN は早い質問返信が浮上の鍵）

---

## anti_patterns チェック（事前セルフ）

- ❌ 機能羅列型: 「Why X」3 つで体験文に転換済み → OK
- ❌ AI 自慢型: 「Build process」段で「設計は人間 / 実装は AI」と所在を明示 → OK
- ❌ 過剰な太字 / 絵文字: マークダウン HN ではプレーンテキスト → OK
- ❌ 思想出しすぎ: 「映す世界を間違えた」「世界平和」は完全に裏 → OK

---

## playable-gate 起動コマンド

```bash
/playable-gate bobrain --target .launch-drafts/show-hn-draft.md
```

通過後の作業:
1. タイトル 1 つ確定
2. 本文を `humanizer-ja` で 1 回通す（projects/CLAUDE.md スタイロメトリー対策）
3. `/wiki-ingest` で raw → analyses/ 反映
4. ローンチ直前にコメント返信用 FAQ も draft 化（別ファイル）
