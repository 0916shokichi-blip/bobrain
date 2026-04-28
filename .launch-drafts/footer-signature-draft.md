# footer 署名ドラフト（playable-gate 通過前の素材）

**目的**: README / LP / Show HN 投稿の末尾に添える「by ぼぶ」署名の候補。projects/CLAUDE.md「モード A: 人格は footer の 1 行で滲ませる」と整合。

**根拠**:
- リサーチ raw: `Documents/マネタイズ/raw/AI 駆動 OSS ローンチ戦略と匿名開発者ブランド構築 2026-04-28.md`「成功したディスクロージャー」表「署名としての by ぼぶ」「同じ作者の新作としてのブランド認知」
- projects/CLAUDE.md: bobrain は「character-universe / bob-universe の架け橋的な存在」（Bob はぼぶの脳の擬人化）

**配置候補**:
- (1) README の最終行（License セクションの直下）
- (2) LP `docs/index.html` の `<footer>`
- (3) Show HN 投稿本文の末尾

---

## 候補（5 案）

### A. リサーチ忠実型 — 「次が来る」明示
> _by ぼぶ — part of the upcoming bob-universe_

- **狙い**: 連続ローンチを期待値として張る、HN/PH の「同じ作者の新作」効果を狙う
- **弱み**: bob-universe は未デプロイ。実体ができる前に名前だけ出すと「空手形」感。**再評価必須**
- **適用先**: 全配置で OK だが、bob-universe デプロイ後に解禁が望ましい

### B. 最小型 — 1 単語
> _by ぼぶ_

- **狙い**: 余計な情報を削り、署名の役割だけに絞る
- **弱み**: 連続ローンチの示唆がない、リサーチ推奨の「next product を匂わせる」効果ゼロ
- **適用先**: 全配置で OK、最も保守的

### C. キャラクター連携型 — character-universe を匂わせる
> _by ぼぶ — Bob is one of a small family of characters_

- **狙い**: character-universe（5 体）の存在を文末で示し、character-gallery への動線になる（character-gallery は未公開だが、いずれ立つ）
- **弱み**: 「characters」が読者には何のことか分かりにくい、説明されない情報の置き残しが気持ち悪く感じる読者もいる
- **適用先**: README ✅ / LP △ / Show HN ❌（HN の作法的に重い）

### D. 架け橋型 — 抑制した連続性
> _by ぼぶ · the brain in a small connected universe_

- **狙い**: bobrain の Bob = 脳キャラだから「the brain」と掛けつつ、connected universe（bob-universe / character-universe 両方）の 1 員と示唆
- **弱み**: 詩的に寄りすぎ、HN/PH の中立トーンとずれる
- **適用先**: LP のみ ✅ / README △ / Show HN ❌

### E. URL ハンドル添え型 — 最も実用的
> _by ぼぶ · github.com/0916shokichi-blip_

- **狙い**: ハンドル名で他作品（philosophy-chat, transcribe-bird, exit-8-homage）への動線を提供。ぼぶブランドの「フォロー先」を 1 つ確定
- **弱み**: GitHub アカウント名 `0916shokichi-blip` に「shokichi」が残る匿名化リスク（bobrain CLAUDE.md L59 既知の問題）
- **適用先**: rename 後なら全配置で ✅、現状は ❌

---

## 推奨

**段階運用**:
1. **今すぐ（Show HN 投稿時点）**: **B（最小）** を README footer + Show HN 本文末尾に。「by ぼぶ」だけで。連続ローンチの示唆は今は出さない
2. **bob-universe デプロイ後（おそらく次フェーズ）**: A に切り替え（projects/CLAUDE.md の bob-universe-hub LP が立った時）
3. **character-gallery 公開後**: C か D を LP のみに採用
4. **GitHub アカウント rename 後**: E を README に採用

理由:
- リサーチは「期待感醸成」を推奨するが、空手形は projects/CLAUDE.md「迷ったら書かない、沈黙の方が哲学の方向性と整合する」と矛盾
- B は引き算の選択。bob-universe / character-universe の存在は、ぼぶの他リポを辿った人だけが気づく構造に留める

---

## anti_patterns チェック（事前セルフ）

- ❌ 思想出しすぎ: 「映す世界」「世界平和」「沈黙」は完全に裏 → OK
- ❌ 機能羅列: 署名なので該当しない → OK
- ❌ AI 自慢: 「Built with Claude」のような署名は弱気な依存に見える → 入れない（disclosure 段で扱う）
- ❌ 空手形: 「coming soon」「stay tuned」は約束として残るので避ける → 推奨案 B はクリア

---

## playable-gate 起動コマンド

```bash
/playable-gate bobrain --target .launch-drafts/footer-signature-draft.md
```

通過後の作業:
1. README.md の `## License` 直下に推奨案 B を 1 行追加
2. `docs/index.html` の `<footer>` に同案を反映（バイリンガル: 日本語側「by ぼぶ」、英語側 "by ぼぶ"）
3. Show HN 投稿本文末尾に追加
