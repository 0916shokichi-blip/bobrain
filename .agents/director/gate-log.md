# Playable Gate 判定ログ

playable-gate v2.0.0 の判定蓄積。5 件蓄積で anti_patterns.md への昇格候補が出る。

---

## 2026-05-19 13:50 target=.launch-drafts/show-hn-final-v3.md

- diff: v2 「OAuth edge case」具体冒頭 + Three things → v3 「years ago に答えてた」抽象冒頭 + Two things + LP hero echo + MCP agent builder 段落
- anti_patterns: ✅ 全 6 カテゴリ通過
  - C1 思想言明なし（「映す世界を間違えた」直書きなし、3 result 例で体現）
  - C2 競合名指しゼロ（Engraph / obsidian-brain / vaultforge / mcpvault 削除済）
  - C3 "No telemetry. Not even error reporting." 独立 punch
  - C4 機能羅列なし、棄却 2 件（summarize しない / send しない）
  - C5 末尾「— ぼぶ」のみ、本文中はモード A
  - C6 アプリツリー横断ルール抵触なし
- Gamma: 採用「内容固有性で構造借用を打ち消し」
  - 構造借用: 「I keep asking X questions I already answered Y」型は Show HN 平均テンプレ
  - 内容固有性: 「years ago」「always already there」が README/LP hero「already wrote it, years ago」と固有 echo、Example query の 3 result が project 固有設計
- 引き算案: n/a（採用）
- 過去類例: v2「Three things」→ v3「Two things」で self-help 三点セット軸 3 弱化、memory `gamma_self_check_overreaction` 機械化準拠
- 人間: YES「価値が surface し、LP hero と一貫」

---

## 2026-05-19 13:55 target=.launch-drafts/reddit-localllama.md

- diff: 旧「workflow gap に困っていた」+ Three things + 競合言及 → v3 整合「years ago に答えてた」+ Two things + MCP-first 段落 + 「multilingual RAG that actually handles non-English」punch
- anti_patterns: ✅ 全 6 カテゴリ通過
  - C1 思想言明なし
  - C2 cloud バッシング軽め、Ollama / Docker 不要は地雷回避として明示（同 sub 文脈で機能訴求の範囲、思想言明ではない）
  - C3 "No telemetry — not even error reporting" 維持
  - C4 stack 詳細 5 ブレットは sub 文脈で「ヲタ層への餌」= 機能羅列ではなく対話の入口
  - C5 末尾「— ぼぶ」のみ
  - C6 アプリツリー横断ルール抵触なし
- Gamma: 採用「sub 作法準拠 + v3 核 punch 維持」
  - 構造借用: 「Hey r/X — sharing what I built」型は Reddit 平均テンプレ
  - 内容固有性: 「multilingual-e5」「in-process」「rank-bm25 with MeCab」が同 sub の embedding 層に固有訴求、HN v3 の冒頭核 punch を維持
- 引き算案: n/a（採用）
- 過去類例: HN v3 と同日判定、positioning 一貫
- 人間: YES「sub 作法と v3 一貫性の両立」

---

## 2026-05-19 13:58 target=.launch-drafts/reddit-obsidianmd.md

- diff: 旧「I know I wrote this somewhere」+ Three things + 競合 4 件名指し → v3 整合「years ago に答えてた」+ Two things + 「Why it's a separate process, not a plugin」独立段
- anti_patterns: ✅ 全 6 カテゴリ通過
  - C1 思想言明なし
  - C2 競合名指し全削除（Engraph / obsidian-brain / vaultforge / mcpvault / mcp-obsidian / obsidian-mcp-tools 全部消した）
  - C3 "100% local, in-process via ONNX. No telemetry. Not even error reporting." 1 行集約 punch
  - C4 stack 5 ブレットは PKM 層への訴求、棄却 Two things で機能否定をバランス
  - C5 末尾「— ぼぶ」のみ
  - C6 アプリツリー横断ルール抵触なし
- Gamma: 採用「sub プラグイン文化への antithesis を内容固有性で支える」
  - 構造借用: 「Hi r/X — sharing something I built」型は Reddit 平均テンプレ
  - 内容固有性: 「Obsidian doesn't need to be running, you don't need the Local REST API plugin」は r/ObsidianMD 固有のプラグイン依存常識に対する反論、bobrain 固有設計
- 引き算案: n/a（採用）
- 過去類例: HN v3 / r/LocalLLaMA v3 整合、3 媒体一貫
- 人間: YES「Vault 文脈で読まれる + plugin antithesis が立つ」

---
