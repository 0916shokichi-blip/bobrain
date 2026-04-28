# Awesome MCP 系リスト PR ターゲット候補（調査ドラフト）

**目的**: bobrain を MCP エコシステムの主要キュレーションリストに掲載するための PR ターゲット選定。リサーチ raw のアクション #6「Awesome MCP リストに PR」を実行可能な状態に落とし込む。

**根拠**:
- リサーチ raw: `Documents/マネタイズ/raw/AI 駆動 OSS ローンチ戦略と匿名開発者ブランド構築 2026-04-28.md`「【仕込み】MCP エコシステムへの積極的な相乗り」
- WebSearch 2026-04-28 実施

**注意**: 各リストの掲載基準は変動が早い。PR 送信前に CONTRIBUTING.md / README の最新版を再確認すること。

---

## 候補一覧

### Tier 1（PR 必須、最も流入が見込める）

#### 1. punkpeye/awesome-mcp-servers
- URL: <https://github.com/punkpeye/awesome-mcp-servers>
- 種類: GitHub README ベース、カテゴリ分けあり
- 規模: コミュニティ最大級（star 数最多のキュレーション）
- 手順: fork → branch（`add-bobrain` 等）→ README.md の該当カテゴリにアルファベット順で挿入 → PR
- CONTRIBUTING: <https://github.com/punkpeye/awesome-mcp-servers/blob/main/CONTRIBUTING.md>
- カテゴリ候補: **「Search & Data Extraction」または「Knowledge & Memory」**（要確認、現行カテゴリ名に合わせる）
- 推奨提出文（短文）:
  > **bobrain** ([0916shokichi-blip/bobrain](https://github.com/0916shokichi-blip/bobrain)) – Local-first hybrid (BM25 + multilingual-e5) RAG MCP server for searching Obsidian vaults and code repos in one query. Japanese-aware out of the box.

#### 2. wong2/awesome-mcp-servers
- URL: <https://github.com/wong2/awesome-mcp-servers>
- 種類: GitHub README ベース、古参
- 規模: 大
- 手順: fork → 該当セクション挿入 → PR（CONTRIBUTING 明示記述は punkpeye ほど厳格でない）
- カテゴリ候補: **Knowledge / Memory / RAG 系のカテゴリを確認**

#### 3. appcypher/awesome-mcp-servers
- URL: <https://github.com/appcypher/awesome-mcp-servers>
- 種類: production-ready / experimental に分類
- 推奨セクション: **experimental**（bobrain は CLAUDE.md L9 で「early prototype」明記済みのため）

### Tier 2（PR 不要、自動収集 / 時間経過で拾われる）

#### 4. tolkonepiu/best-of-mcp-servers
- URL: <https://github.com/tolkonepiu/best-of-mcp-servers>
- 種類: 自動収集型、GitHub stars / package manager メトリクスで週次自動ランキング
- アクション: **PR 不要**。bobrain の GitHub stars が上がれば自動的に拾われる
- 確認: 数週間後に検索して掲載されているかチェック

### Tier 3（要詳細調査、後回し）

#### 5. modelcontextprotocol/servers（公式）
- URL: <https://github.com/modelcontextprotocol/servers>
- 種類: 公式リファレンス実装中心
- 注意: **サードパーティ MCP の掲載基準は要確認**。「Reference servers」と「Community servers」のセクション分けがあるかどうか
- 最初は punkpeye 等の Tier 1 で実績を作ってから検討

#### 6. mcp.so
- URL: <https://mcp.so/>
- 種類: ウェブディレクトリサイト
- 登録方法: 要調査（GitHub PR or Web フォームか不明）
- 後回し OK

#### 7. mcpservers.org
- URL: <https://mcpservers.org>
- 種類: ウェブディレクトリサイト
- 登録方法: 要調査
- 後回し OK

#### 8. TensorBlock/awesome-mcp-servers / patriksimek/awesome-mcp-servers-2
- 種類: 同名フォーク系
- 優先度: Tier 1 完了後に余力で

---

## 推奨実行順序

1. **Show HN ローンチと同じ日**に Tier 1 の 3 リストへ並列 PR
2. PR 提出前に GitHub Social Preview 画像（CLAUDE.md L76 の残タスク）を完了しておく — リスト経由で訪れた人が見るのは GitHub repo
3. Tier 2 は放置で OK（自動収集を待つ）
4. Tier 3 は Show HN で 100+ star を獲得してから検討

## 提出文 標準フォーマット（再掲）

```
**bobrain** ([0916shokichi-blip/bobrain](https://github.com/0916shokichi-blip/bobrain)) – Local-first hybrid (BM25 + multilingual-e5) RAG MCP server for searching Obsidian vaults and code repos in one query. Japanese-aware out of the box.
```

- 文字数: 約 230 文字（多くの awesome list の慣例 = 1 行に収まる長さ）
- アルファベット順での挿入位置: 「b」のセクション、「bobrain」は通常 `bilibili-mcp` の後あたり
- 「early prototype」「Status: alpha」表記が明示的に必要なら、そのリストの慣例に合わせて追加

---

## 注意事項

- **PR 1 件ずつ慎重に**: 同時に 3-4 リストへ PR を投げると「prolific submitter」と見なされて却下されるリスク。1 つ目をマージしてから次に進むのが安全
- **bobrain README とフォーマット一貫性**: awesome list の説明文は README ヒーロー文と矛盾しないこと（CLAUDE.md L20 のキラーメッセージとの整合）
- **匿名性**: GitHub アカウント `0916shokichi-blip` の「shokichi」表記は当面残る（CLAUDE.md L59 既知問題）。awesome list の PR コミットメッセージにも「ぼぶ <noreply>」が出ることを事前確認

---

## 次のアクション

- [ ] Show HN ローンチ日確定
- [ ] punkpeye/awesome-mcp-servers の README.md を実際に開いてカテゴリ名と挿入位置を特定
- [ ] その日に PR を 1 件出す（残り 2 件は翌日以降）
- [ ] mcp.so / mcpservers.org の登録手順を別途調査（後日）
