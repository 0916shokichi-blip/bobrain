# Phase 3 #4 — Lab Pass 実装計画

**経緯**: 2026-05-09 commune-loop で「Bobrain Lab Notebook」道筋を創発、パターン α (Show HN 予定通り + Notebook + Lab Pass は post-Show HN follow-up) を採用。本計画は Show HN ローンチ後の **Lab Pass 形態での Phase 3 #4 決済先行実装** の手順書。memory `payment_mor_provider_split` (5/1) + log.md L453-508 (5/9 commune パターン α) の統合。

**Pro 版本格化は Lab Pass の N=1 検証後に判断** (memory rational default 3,000 円買い切り路線も保留中)。

---

## 戦略全体

### Lab Pass モデル

- **closed beta**: 「同じ構造を作りたい」と Notebook 末尾で発話した読者を招待
- **価格 rational default**: $5-10/月 (Early Bird 判定後決定、user 専権)
- **提供物**: bob_persona dogfood 結果共有 (匿名) + closed Discord/GitHub Discussions + Notebook 早期アクセス + Phase 2 残機能 (heading chunking / CoreML) 早期試用
- **思想整合**: Obsidian 型「データ所有権無料 + 摩擦削減有料」、PostHog/Excalidraw 型バイヤー中心オープンコアではない

### Notebook 連載との連動

- Show HN KPI 観察結果が出た直後、**Notebook 1 本目「8 アプリ tree 1 角度目」** 執筆
- 月 1-2 本、`docs/lab/` 配下、bob_persona fictional dogfood シナリオ
- **3 本完走時に Lab Pass beta 募集開始**
- 各記事固定フォーマット: 検索前の問い → bobrain 検索結果 → 過去ログ再発見 → 「同じ構造を作りたい」発話

### Phase 2 残機能との連動

- **#6 heading chunking (Marko AST)** = OSS、Notebook 駆動で実装
- **#7 CoreML 高速化** = OSS rational default、Notebook 駆動で実装
- 機能追加が連載ネタになる compound、改造のたび `/playable-gate` L4 関門

---

## Phase 4a: 法務 + 決済インフラ (Notebook 連載と並行)

### 1. NAWABARI バーチャルオフィス契約

- **料金**: 月 1,100 円
- **申込**: <https://www.nawabari.net/> → 屋号「Bobrain Labs」+ 留守電音声メール転送
- **GPS 混入チェック**: 実装済 (memory `payment_mor_provider_split` 確定スタック)
- **取得物**: 住所 (特商法表示用) + 屋号宛郵便受領
- **完了マーカー**: NAWABARI 契約書 PDF を `~/.private/business/` (gitignore) 保管

### 2. GMO あおぞらネット銀行屋号付き口座開設

- **料金**: 同行宛無料 / 他行 143 円
- **申込**: 個人事業主屋号付き、Selfie 動画認証 → 通常 1 週間、運良ければ即日
- **Polar.sh 着金経路**: Stripe Connect Express → GMO あおぞら屋号付き口座 → 個人口座 (必要時のみ移動)
- **完了マーカー**: 口座番号 + 屋号確認の log.md エントリ (口座番号自体は非公開)

### 3. Polar.sh アカウント作成 + KYC

- **手数料**: 4% + $0.40
- **登録**: <https://polar.sh/> → GitHub 連携
- **Display Name** (表示用) = NAWABARI 表示住所
- **Business Address** (KYC 用) = **書類通りの本住所** (非公開、memory 地雷 8 回避)
- **W-8BEN 電子署名**: ダッシュボード上で完結、IRS 直接やり取り不要
  - **必須**: 最初の売上が立つ前に署名済ませる (memory 地雷 3、30% 源泉徴収回避)
- **完了マーカー**: Polar dashboard で "Verified" 表示 + W-8BEN signed status の screenshot を `~/.private/business/` 保管

### 4. 特商法ページ作成

- **販売主体**: Polar Software Inc. (海外 MoR、適格請求書発行事業者ではないが国外事業者区分)
- **提供元**: 個人事業主 X (匿名運用、住所・電話番号は請求に基づき遅滞なく開示)
- **配置**: LP `docs/index.html` 末尾に「特商法表記」link → `docs/legal/tokushoho.html` 新規作成 (or 既存 `disabled-2026-05-13/philosophy-chat-legal/tokushoho.md` をテンプレ流用)
- **memory `payment_mor_provider_split` 定型文準拠**

### 5. インボイス制度対応判断

- **2026-10-01 で経過措置 80% → 50%、2029-10 で 0%**
- **判断軸**: 個人事業主のまま課税事業者選択 (簡易課税 or 本則課税) vs 免税継続
- **B2B 訴求**: LP 文言で「Polar.sh 経由 (海外 MoR)」明示で個人インボイス未登録の影響緩和
- **timing**: Lab Pass N=1 検証後、Pro 版本格化判断と同時に再評価

---

## Phase 4b: bobrain 側実装 (Lab Pass mechanism)

### 1. License Key validate 統合

- **API**: Polar `/v1/customer-portal/license-keys/validate` (認証なしで呼べる = CLI 最適、memory CLI 認証方式の第一選択)
- **24h grace period**: オフライン環境でも 24 時間は Pro 機能利用可 (memory 地雷 9 回避)
- **Activation Limit**: 1-3 デバイスに制限 (濫用防止)
- **保管**: Python `keyring` (macOS Keychain / Windows Credential Locker / Linux Secret Service)、**平文 yaml/json 保存禁止**
- **CLI**: `bobrain auth login` (License Key 入力) / `bobrain auth status` (validate 結果)

### 2. Webhook handler

- **route**: `/api/webhook/polar` (Next.js App Router、LP と同じ Vercel project に追加 or 別 serverless)
- **middleware 除外**: CSRF / 認証 middleware の matcher から明示除外 (memory 地雷 5 回避)
- **処理**: **即 200 OK 返却 → Redis (Upstash) / QStash で非同期実行**
- **重要 event**:
  - `subscription.created`: 自社 DB に Pro flag set
  - `subscription.revoked`: Pro flag 取消 (返金時の Pro 継続バグ防止、memory 地雷 7)
  - `license_key.created`: keyring 保管推奨を email で通知
- **再配信**: 順序保証崩れる点に注意 (memory 地雷 5)

### 3. external_customer_id 固定

- **Checkout 生成時**: `external_customer_id` = 自社 DB user_id (固定値、memory 地雷 6 回避)
- **Better Auth 利用時**: `@polar-sh/better-auth` プラグインで自動連携
- **複数回購入対応**: アップグレード時の Entitlement 集約破綻を予防

### 4. MCP list_tools 動的生成

- **無料**: search / index / status 等の基本ツール
- **Lab Pass 限定**: `lab_benchmark_contribute` (匿名 dogfood 結果共有) / `lab_early_access_feature` (Phase 2 #6/#7 早期試用)
- **ライセンス確認**: `validate_response.granted` ベースで MCP `list_tools` レスポンス生成

### 5. CLI 統合

```
bobrain auth login          # License Key 入力 → keyring 保管 → validate
bobrain auth status         # 現在の Pro flag + activation device count
bobrain auth logout         # keyring 削除
bobrain lab benchmark       # Lab Pass 限定: 匿名 dogfood 結果送信
```

---

## Phase 4c: Lab Pass 機能定義 (Notebook 1 本目執筆後に詰める)

### Lab Pass beta tester への提供物 (rational default)

1. **benchmark contributor**: bob_persona dogfood 結果を匿名で共有 → 全 Lab Pass member 閲覧可
2. **closed Discord / GitHub Discussions**: Lab Pass 限定 channel、bobrain 開発議論
3. **Notebook 早期アクセス**: 一般公開 1 週間前に Lab Pass member へ
4. **Phase 2 残機能早期試用**: #6 heading chunking / #7 CoreML 高速化を OSS リリース前にアクセス可
5. **bob_persona 直接対話**: 月 1 回 (?)、Lab Pass member の質問に bob_persona が回答 (要検討)

### 招待制 mechanism

- Notebook 末尾「同じ構造を作りたい」発話を **GitHub Discussions / form 経由で記録**
- 集約後、user 手動で invite (closed beta = 招待制維持)
- Polar.sh: invite-only Checkout (URL を Lab Pass member にのみ配布) or discount code 100% off 招待

### 価格決定保留中の事項 (user 専権)

- $5/月 vs $10/月: Show HN KPI + Notebook 反応で判断
- 年額割引: $50/年 (2 ヶ月分 free) を default 提示?
- Lifetime: 当面なし (memory log L163 の $49 LTD 案は 5/9 commune で却下、Lab Pass 月額路線確定)

---

## Phase 4d: Notebook 連載準備

### 1 本目「8 アプリ tree 1 角度目」テンプレ

- **題材**: Show HN KPI 観察結果 + cross_project_philosophy 骨格 1「8 アプリ = 面の 8 つの角度」の 1 角度を bob_persona dogfood シナリオで描く
- **形式**: 検索前の問い (bob_persona の悩み) → bobrain 検索結果 (notes + code namespace) → 過去ログ再発見 (実体験エピソード化) → 「同じ構造を作りたい」発話 (Lab Pass 招待 hook)
- **配置**: `docs/lab/2026-XX-XX-app-tree-angle-1.md` (Vercel LP build 経路で `/lab/` 配下に site 化)

### 連載構成 (rational default、user 確認保留)

- **月 1-2 本** (heavy = 月 1、軽め = 月 2)
- 全 8 角度 (8 アプリ = 面の 8 つの角度) を 1 本ずつ → 4-8 ヶ月で完走
- 3 本完走時に Lab Pass beta 募集開始

### PII 回避

- bob_persona = fictional persona シナリオで担保
- 実 Vault path / 実 commit ID は伏せる (Show HN KPI は本物の数字を使う = transparency)

---

## リスク + 地雷参照 (memory `payment_mor_provider_split` 統合)

| 地雷 | 影響 | 回避策 (本計画該当箇所) |
|---|---|---|
| 1. Polar PayPal 未対応 | Lab Pass = 開発者向け = 影響軽微 | 一般消費者向け philosophy-chat 用 Lemon Squeezy 検討は別軸 |
| 2. 2026-10 インボイス経過措置 | B2B 訴求の影響 | LP に「Polar.sh 経由 (海外 MoR)」明示、Phase 4a §5 |
| 3. W-8BEN 未提出で 30% 源泉徴収 | 米国売上に直撃 | Phase 4a §3 で最初の売上前に署名 |
| 4. 特商法表示と匿名運用 | 住所公開リスク | Phase 4a §4 で NAWABARI + MoR 二段防御 |
| 5. Webhook 10 連続失敗で自動 Disabled | Pro flag 更新失敗 | Phase 4b §2 で middleware 除外 + 即 200 OK + 非同期 |
| 6. external_customer_id 未指定で Customer 重複 | Entitlement 破綻 | Phase 4b §3 で固定値渡し |
| 7. 60 日 Polar 独自返金権 | 返金時の Pro 継続バグ | 利用規約に「原則返金不可」+ subscription.revoked Webhook で取消 |
| 8. KYC 住所不一致で手動レビュー詰まり | 開設遅延 | Phase 4a §3 で Business Address = 本住所、Display = NAWABARI |
| 9. License Key オフライン検証不可 | Pro 機能利用不能 | Phase 4b §1 で 24h grace period + activate bind |

---

## 実装順序 (相対表現、外的締切なし)

1. **Show HN 投稿実施 + 90 分張り付き** (Phase 3 #3 完了)
2. **Show HN KPI 観察 1-2 ヶ月** (memory `showhn_launch_benchmarks_2026` 準拠)
3. **Notebook 1 本目「8 アプリ tree 1 角度目」起草** (KPI 反映)
4. **Phase 4a §1-2** (NAWABARI + GMO 銀行) を Notebook 執筆と並行
5. **Phase 4a §3-4** (Polar アカウント + 特商法) — Notebook 1 本目公開前後
6. **Notebook 2-3 本目執筆** (各角度を順次)
7. **Phase 4b** (bobrain 側実装) — Notebook 3 本目公開前に完成目標
8. **Lab Pass beta 募集開始** — Notebook 3 本完走時
9. **Lab Pass N=1 検証** (1-2 ヶ月)
10. **Pro 版本格化判断** (Lab Pass N=1 結果から rational default 3,000 円買い切り路線復活 or 別形態)

---

## ledger / 監査

- 各 step の log.md エントリ (Phase 3 #4 タグ統一)
- 簡易売上 ledger: `~/.private/business/sales-ledger-2026.md` (gitignore)
- 月次 reconciliation: Polar dashboard + GMO 銀行残高 + ledger の三角照合
- 税務記録: 仕訳 + 領収書を `~/.private/business/tax-records/` で年単位整理
- インボイス制度判断は 2026-10 経過措置前に user 専権で再判断

---

## 関連 memory + ファイル

- memory `payment_mor_provider_split` — 本計画の原典 (9 地雷 + 実装パターン)
- memory `bobrain_pypi_launch` — PyPI 公開地雷集 (同様の標準フロー系)
- memory `cross_project_philosophy` — Lab Pass 思想整合 (Obsidian 型データ所有権)
- log.md L453-508 — 5/9 commune パターン α 確定の経緯
- `.launch-drafts/show-hn-final-humanized.md` Q5 — Pro 版言及 (Phase 4 で検討中、Polar.sh 想定)
- `.launch-drafts/phase3-3-user-operations.md` — Phase 3 #3 投稿前 user 操作 (本計画の前段)

---

## 次のアクション (本計画完成後)

- **本計画書を bobrain repo に PR 投入** (Phase 3 #3 deliverables と同経路)
- **CLAUDE.md L85-93 Phase 3 #4 方針を本計画書への link に置換** (詳細化、内容 drift を 1 箇所に集約)
- **Show HN 投稿実施まで本計画は dormant** (post-Show HN で着手)
