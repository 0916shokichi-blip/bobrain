# r/ObsidianMD draft (v0)

起草日: 2026-04-28
投稿想定: 5/6 水曜 米東部 9-11 AM = 日本時間 水曜 22-24 時（Show HN / r/LocalLLaMA の翌日にずらす）
推敲ステータス: marketer-ja 起草版、未 playable-gate / 未 humanizer-ja

## title

```
I built a local search server that finds answers across my Obsidian vault AND my code repos in one ranked list
```

## body

```markdown
Sharing something I made for myself, in case anyone has the same itch.

The thing I kept hitting: I'd half-remember writing about a topic — and I
genuinely couldn't tell whether it was in my Obsidian vault or buried in a
README from a side project two years ago. So I'd search the vault, find
nothing, then `grep` through old repos, find a mention, then realize the
real note was actually in the vault under a different title.

The answer I was looking for, I had already written. I just couldn't find
where.

So I built **Bobrain**: a local search server that indexes my vault AND
my Git repositories into one ranked list, and exposes it to Claude /
Claude Desktop / Cursor through MCP. Now I can ask "where did I write
about MCP chunking strategies — in my notes or the code?" and get one
list across both.

A few things that might matter to fellow Obsidian users:

- **Fully local**. No cloud, no API calls. ONNX runs the embedding model
  on your machine.
- **Hybrid search** — BM25 (with proper Japanese tokenization, since I
  write bilingually) plus semantic embeddings, fused. Catches both exact
  terms and meaning.
- **Doesn't touch your vault**. Read-only indexing. Doesn't modify
  Markdown, doesn't add frontmatter, doesn't sync anywhere.
- **Doesn't replace Obsidian's built-in search** — it's for the cases
  where you want one search across your vault and your other Markdown /
  code sources. For everyday "find this note" queries, Obsidian's
  built-in is still better and faster.

**Honest status**: this is an early prototype I released as 0.1.0
yesterday. Markdown-only today. PDF support and smarter code chunking are
on the roadmap. MIT licensed and free. There may be a Pro version later
for sync / multi-machine, but the core stays open.

Install: `pipx install bobrain` or `uvx bobrain`
Repo & docs: https://github.com/0916shokichi-blip/bobrain

If you've felt the "I know I wrote this somewhere" frustration across
your vault and other places, I'd love to hear if this fits the workflow
or misses it.

— ぼぶ
```

## 投稿先別の注意点

- **投稿時刻**: r/ObsidianMD は土日昼〜夕方（米東部）が伸びやすいが、平日夜（日本時間 火曜 22-24 時 = 米東部 9-11 AM）も悪くない。Show HN / LocalLLaMA との同日連投は避け、**翌日（水曜）にずらす** のを推奨
- **self-promotion**: r/ObsidianMD は商用色に敏感。Pro 版に触れたが「未公開」「OSS core stays open」を明示。ここを誤ると即削除される
- **PKM コミュニティの作法**: 技術深掘りより **「実際のワークフローでどう使うか」** が読まれる。本文の「Killer use case → 1 ranked list across both」を一番太く書いた
- **footer "— ぼぶ"** は唯一ここだけ滲ませた。PKM はハンドル文化が許容されやすい。Show HN / LocalLLaMA は無記名でプロダクト中心
- **初動で答えるべき暗黙の質問**: (1) Smart Connections / Copilot for Obsidian と何が違うのか (2) Vault のデータをどう扱うのか（プライバシー） (3) MCP って何

## 想定 Q&A（初動 90 分用）

1. **Q**: How is this different from Smart Connections or Copilot for Obsidian?
   **A**: Those are excellent for in-vault Q&A and stay inside Obsidian. Bobrain is built for the case where your knowledge isn't only in the vault — it's also in code repos, README files, design docs across other folders. If your workflow is purely vault-centric, Smart Connections is probably the better fit. Bobrain shines when you straddle notes and code.

2. **Q**: Does it modify my vault or sync anything?
   **A**: No. Read-only indexing. It doesn't write to your Markdown files, doesn't add frontmatter, doesn't sync anywhere. The index lives in a separate SQLite + files directory you control.

3. **Q**: I don't use Claude / Cursor — is this useful for me?
   **A**: Honestly, less so right now. The CLI works (`bobrain query "..."`) but the main UX win is the MCP integration with assistants. If you're not using an MCP-compatible client, the value drops a lot. I'd wait for v0.2 when CLI / web UI improvements land.

4. **Q**: What about PDFs? I have a lot of papers.
   **A**: On the roadmap, not shipped yet. Today: Markdown only. PDF ingestion is the next major feature.

5. **Q**: Will the Pro version put core features behind a paywall?
   **A**: No. The OSS core (indexing, hybrid search, MCP server, CLI) stays MIT and free. Pro, if it happens, would be sync / multi-machine / hosted backup — things I can't reasonably ask people to self-host. Nothing is announced or available yet.

## 気をつけたこと（anti_patterns 回避メモ）

- **機能羅列を避けた箇所**: 「困った状況の具体描写」を本文の半分まで使い、技術スタックは "Hybrid search" の 1 行に圧縮した。PKM コミュニティは「使い心地」が読みたい
- **誇大表現を避けた箇所**: "Doesn't replace Obsidian's built-in search" "For everyday queries, Obsidian's built-in is still better and faster" と **明示的に劣る場面を書いた**。これは self-promotion 警戒の解除装置にもなる
- **体験文に寄せた箇所**: 「The answer I was looking for, I had already written. I just couldn't find where.」を独立した 1 段落にした。Hero copy の英語版 "you already wrote it, years ago" を**そのまま使わず、文脈に溶かして** 1 度だけ出した
- **哲学を出さなかった箇所**: 「映す世界」「解釈」「世界平和」は完全に沈黙。代わりに「I had already written. I just couldn't find where.」という日常的な悔しさだけ残した
- **footer "— ぼぶ"** はあえて漢字 / カタカナでなくひらがな 2 文字。匿名運用と整合する最小限の人格痕跡

## 改稿で迷ったら削るポイント

- "The answer I was looking for, I had already written. I just couldn't find where." が hero copy 引用と感じられたら 1 文に圧縮
