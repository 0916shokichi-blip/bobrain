# Show HN v2 — value surface rewrite (2026-05-19)

**経緯**: v1 humanized (show-hn-final-humanized.md) は anti_patterns + Gamma + humanizer-ja の 3 段関門通過済だったが、user の「価値が surface してない」発話で再診断。L0 vision「Obsidian の高速検索 / 機能説明にしか聞こえない / 競合羅列」の 3 つの avoidance に v1 が抵触していたと判明。v2 は具体的 query 例 + killer line ("Claude doesn't know what I already wrote") + WHY 付き制約列挙で「立ち止まらせる強度」を狙う。

**rewrite 軸**:
- 痛み = 抽象 → 直近の具体的事件 (OAuth edge case)
- killer line 追加: "Claude doesn't know what I already wrote."
- アーキ説明 (BM25/MeCab/e5/RRF) を段落丸ごと → 末尾 Q&A 誘導 1 行に圧縮
- 競合 4 件名指し → 削除、implicit な対比のみ
- 「3 things doesn't do」を機能否定 → WHY 付与で価値の証明に転換
- 具体的 query → 3 件の result 例で「過去の自分との対話」を直接書かず体現

**L0 vision 整合チェック**:
- ✅「直接書かない」維持 (変容的体験を 言葉で 説明しない)
- ✅「過去の自分の足跡」を「Q + result 3 件」で 体現する
- ✅「便利ツール」/「第二の脳」/「Obsidian の高速検索」位置付けに該当しない
- 要 Gamma 再走 (L4 関門必須)

---

## タイトル (76 文字、変更なし)

```
Show HN: bobrain – A local MCP that searches my notes and code repos together
```

## 本文 (v2)

```
Last week I needed to recall how I'd handled a particular OAuth edge case. I knew I'd solved it before — but was the answer in my Obsidian decision log? Or buried in some README from a 2023 branch I'd long since deleted from my head? Searching both meant grepping in two places, with two different mental models. So I kept asking Claude instead. Which is worse, because Claude doesn't know what I already wrote.

bobrain is a local MCP server that fixes this. Point it at any number of directories — your Obsidian vault, your ~/code/, anything markdown or code — and it indexes each as a separate namespace. From Claude / Cursor / Claude Desktop, one query hits all of them.

Example:

  Q: "How did I think about retry/backoff in any of my past projects?"

  → bobrain returns:
    • a chunk from reliability-notes.md (2023)
    • the actual exponential-backoff implementation from a 2022 repo
    • a related Slack paste in my Obsidian inbox

Three things it deliberately doesn't do:
- Summarize what comes back. You see the raw chunk + file path. When you're trying to recall what past-you actually wrote, paraphrase is the enemy.
- Send your notes anywhere. Embeddings run in-process via ONNX. No telemetry. Not even error reporting.
- Lock you to Obsidian. Plain .md files on disk is enough.

Solo project. Design and tests are mine; commits aren't squashed if you want to read along. Claude Code wrote the implementation under those constraints.

Repo: https://github.com/0916shokichi-blip/bobrain
LP: https://0916shokichi-blip.github.io/bobrain/
Install: pipx install bobrain

Happy to dig into the namespace design, the JP tokenizer choice (some of my notes are Japanese), or why I picked e5-large over BGE.

— ぼぶ
```

---

## 投稿前チェックリスト (v1 から引き継ぎ + v2 追加)

- [ ] **playable-gate v2 再走 必須** (anti_patterns + Gamma + L4 人間関門)
- [x] humanizer-ja は v2 起草中で適用済 (textbook 構文 / by design 等は混入させてない)
- [x] og.png upload 完了 (5/19 確認)
- [x] PyPI 0.1.0 fresh venv 動作確認 (5/18)
- [x] SECURITY.md 公開 (5/17)
- [x] branch protection 整備済 + drift 修正済 (5/18)
- [x] Dependabot alerts 全 fixed
- [x] PII 流出修正完了 (5/19、本日 filter-repo + force push 経由)
- [x] GitHub Settings: Keep email private + Block CLI push 両方 ON
- [ ] demo.gif 撮影 (任意、skip OK)
- [ ] Show HN 投稿実行 (gate 通過後)

---

## v1 (humanized) との関係

v1 (`show-hn-final-humanized.md`) は **anti_patterns + Gamma + humanizer-ja の関門通過済**だが「価値 surface 不足」で却下判定。v2 は v1 の関門通過資産を継承しつつ価値訴求を強化、再関門通過後に投稿候補確定。

v1 は archive 用途で残す (gate 通過記録としての価値あり)。v2 が gate 通過したら v2 が投稿テキスト。

---

## 投稿タイミング

本日 (5/19 火) 19-21 JST = HN 黄金時間。v2 gate 通過が間に合えば本日投稿、間に合わなければ次の月火 (5/25 月 or 5/26 火) 19-21 JST へ punt。期限なし運用。
