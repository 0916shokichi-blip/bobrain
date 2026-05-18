# Phase 3 #3 投稿前 user 操作ガイド

Show HN 投稿前に **Claude が代行できない** 2 つの user 操作（og.png upload + GIF 撮影）の手順。Claude 完結タスク（humanizer-ja / PyPI 動作確認）は 2026-05-18 完了済。

---

## 1. GitHub Social Preview 画像 upload（最重要、最短）

**目的**: HN 投稿リンクから訪問者が GitHub repo を踏んだ時、Twitter Card / Slack preview / Discord embed で `assets/og.png` (1280×640) が表示される。

### 手順

1. ブラウザで開く（要 GitHub ログイン）:
   <https://github.com/0916shokichi-blip/bobrain/settings>

2. 下の方の **"Social preview"** セクションを探す（"Optional" と表示されてる）

3. **"Edit"** ボタンクリック → **"Upload an image..."**

4. ファイル選択: `~/projects/bobrain/assets/og.png`

5. Save

**確認**: 投稿前に Slack / X / Twitter で repo URL を貼り付け → preview に画像が出れば成功（GitHub 側のキャッシュは数分で更新）。

### gh CLI 代替経路（REST API 未対応）

GitHub REST API には Social Preview の upload endpoint **無し**。`gh` CLI 経由は不可、Web UI のみ。

---

## 2. 15 秒デモ GIF 撮影（任意、README 用）

**目的**: README 上部に貼って訪問者の理解を 5 秒で成立させる。HN 投稿本文 (`show-hn-final-humanized.md`) に **GIF リンクは含めない方針**（show-hn-final.md L44 既決）。README ヘッダーに置くだけで十分。

### 前提

- Claude Desktop 起動済 + bobrain MCP server 接続済
- `gifski` インストール: `brew install gifski`（未インストールなら）

### 撮影シナリオ（15 秒以内）

1. Claude Desktop で新規セッション開く
2. プロンプト: `bobrain で notes と code namespace を横断 search して、「embeddings」関連の chunk を 5 件取ってきて`
3. Claude が MCP 経由で bobrain.search を呼ぶ → 結果が notes と code 両方から返る
4. 結果リストを 2-3 秒スクロール表示

### 撮影コマンド（mov → GIF）

```bash
# 1. 録画開始 (Cmd+Shift+5 で部分選択モード)
#    または:
screencapture -v -V 15 ~/Desktop/bobrain-demo.mov

# 2. mov → GIF 変換 (24fps, 800px 幅、約 2MB)
gifski --fps 24 --width 800 --quality 90 \
  -o ~/projects/bobrain/assets/demo.gif \
  ~/Desktop/bobrain-demo.mov

# 3. ファイルサイズ確認 (README 上限 5MB 推奨)
ls -lh ~/projects/bobrain/assets/demo.gif
```

### README 反映（撮影後、Claude に依頼可）

`README.md` のヘッダー下に追加:
```markdown
![bobrain demo](./assets/demo.gif)
```

→ commit + PR (main 直 push 禁止のため feature branch 経由)

### プライバシー注意

- 撮影前に Vault path をダミーに置換するか、ターミナルの session を新規にして履歴を出さない
- Claude Desktop の chat 履歴に個人情報が映らない例題プロンプトを選ぶ
- `~/Documents/notes` の実 path は問題なし（公開可能）、`~/code/<project>` も問題なし。具体的なファイル名・コミット内容は伏せる

---

## 3. 投稿実行（user 専権、最終 step）

### 前提（全部 ✅ で投稿可）

- [x] PyPI 0.1.0 fresh venv 動作確認 (2026-05-18)
- [x] SECURITY.md 公開 (2026-05-17)
- [x] branch protection 整備 (2026-05-18 修正済)
- [x] Dependabot alerts 全 fixed
- [x] humanizer-ja 通過 (2026-05-18 完了、`show-hn-final-humanized.md`)
- [ ] **og.png upload** (上記 §1)
- [ ] **demo.gif 撮影 + README 反映** (任意、上記 §2)
- [x] GitHub repo description 整備済

### 投稿テキスト

`~/projects/bobrain/.launch-drafts/show-hn-final-humanized.md` の **L21-44 のコードブロック内をそのまま** 投稿:

- HN: <https://news.ycombinator.com/submit>
  - Title: `Show HN: bobrain – A local MCP that searches my notes and code repos together`
  - URL: `https://github.com/0916shokichi-blip/bobrain`
  - Text: body のみ（最初の paragraph から `— ぼぶ` まで）

- 並行投稿（同日 or 翌日）:
  - r/LocalLLaMA: `.launch-drafts/reddit-localllama.md` の humanize 判定後
  - r/ObsidianMD: `.launch-drafts/reddit-obsidianmd.md` の humanize 判定後

### 投稿後 30 分の運用

memory `showhn_launch_benchmarks_2026` 準拠:

- **0-30 min**: 2 pt 未満なら撤退検討（バックラッシュ avoid）
- **30-60 min**: 5 pt 信頼線、超えたら Q&A 張り付き継続
- **60-90 min**: 倍プッシュ閾値、front page 残留の重大時間帯
- **90 min-12h**: モード A 中立で全質問即答、`qa-arsenal.md` の Q1-Q8 流用

### 投稿後 if-then

- **「Vibe-coded?」質問** → Q6 のテンプレ即答
- **「why local?」質問** → Q3 + philosophy_os 行動記述（直接書かない）
- **競合作者コメント** → vaultforge 比較表と同じ作法で誠実応答
- **バックラッシュ / 党派化** → x-integration.md v0.4 セーフティ「以上。で終える胆力 / 削除しない / 1 週間止める」

---

## まとめ

| ステップ | 必須度 | 時間目安 | Claude 代行 |
|---|---|---|---|
| §1 og.png upload | 必須 | 1 分 | ❌ Web UI のみ |
| §2 GIF 撮影 + README 反映 | 任意 | 10-15 分 | 撮影は user / README 反映 + PR は Claude 可 |
| §3 投稿実行 | 必須 | 5 分 + 90 分張り付き | ❌ user 専権 |

§1 を済ませれば（§2 skip でも）Show HN 投稿可。
