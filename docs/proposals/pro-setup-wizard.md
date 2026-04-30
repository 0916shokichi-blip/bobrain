# Pro 機能設計提案: セットアップウィザード `bobrain init`

**status**: proposal
**target version**: v0.2.0 (Pro)
**author**: ぼぶ
**date**: 2026-04-29
**source**: Gemini DR「ローカルファースト RAG MCP 市場分析」(2026-04-29) の Pro 化候補 #3「設定オートメーション」

## なぜこれが Pro 限定の最有力候補か

### 1. 離脱ポイントとしての強さ

DR が指摘する MCP サーバーの最大離脱ポイントは、ユーザーが各 IDE の設定ファイル（`mcp_config.json` 等）を **手作業で編集** すること。具体的には:

- **Claude Desktop**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Code**: `~/.claude/mcp.json` または project の `.mcp.json`
- **Cursor**: `~/.cursor/mcp.json` または `.cursor/mcp.json`

各ファイルの場所、JSON 構造、再起動の必要性、Path の解決（uv / pipx / system Python）がすべて異なる。

### 2. 既存 Pro 化候補との比較

| 候補 | OSS 状態 | Pro 化の妥当性 |
|---|---|---|
| ハイブリッド検索 (BM25+ベクトル) | **既に OSS 実装済み** | ❌ Pro 化すると downgrade |
| インデックス自動更新 | OSS は手動 `bobrain index` | △ 妥当だが価値が伝わりにくい |
| エージェント書き込み（Vault への新規ノート） | OSS は read-only | △ 妥当だが安全設計が重い |
| **セットアップウィザード** | OSS は手動編集 | ✅ **時間を買う価値が最も具体的** |
| マルチモデル最適化プロンプト | OSS は generic | △ 効果が実測しづらい |

### 3. 「時間を買う」価値の具体性

ユーザーの離脱コストは「30 分の試行錯誤 + フォーラム検索」。Pro $49 LTD でこれを 1 コマンドに圧縮する → 価格と価値が直結する。

## 設計

### CLI インターフェース

```bash
# OSS では手動で mcp.json を書く案内のみ
bobrain init  # → Pro 限定エラー or プレビュー版

# Pro 版
bobrain init --ide=claude-code        # Claude Code 用 .mcp.json を自動生成
bobrain init --ide=claude-desktop     # Claude Desktop の config を自動更新
bobrain init --ide=cursor             # Cursor の config を自動生成
bobrain init --ide=all                # 検出できる IDE 全部に書き込み

# オプション
bobrain init --ide=claude-code --dry-run     # プレビューのみ
bobrain init --ide=claude-code --validate    # 既存 config の妥当性検査
bobrain init --ide=claude-code --uninstall   # 設定除去
```

### 各 IDE の処理フロー

1. **検出**: IDE の設定ファイルパスを OS / 既知の場所から自動検出
2. **バックアップ**: `<config>.bak.<timestamp>` を作成
3. **マージ**: 既存の MCP サーバー定義を保持しつつ bobrain のエントリのみ追加 / 更新
4. **検証**: JSON 妥当性チェック + `bobrain --version` 実行可能性チェック
5. **再起動案内**: IDE 再起動が必要な旨を表示

### ライセンス検証

- OSS 版で `bobrain init` を実行すると「This is a Pro feature. Get a license at <Polar.sh URL>」表示 + `--ide=<...>` のための JSON サンプルを表示（手動コピペできる）
- Pro 版は `~/.bobrain/license.json` または環境変数 `BOBRAIN_LICENSE_KEY` で検証
- ライセンスは Polar.sh の license key API（または OSS で書ける署名付き JWT）で検証

### 含めない（v0.2.0 スコープ外）

- 自動アップデート機構（v0.3.0 以降）
- IDE プラグイン形式での提供（GUI 経由は別問題）
- ライセンスの remote validation（オフラインでも動くべき、ローカル検証のみ）

## 実装スケッチ

```python
# src/bobrain/cli/init.py
from pathlib import Path
import json
import platform
import shutil

IDE_PROFILES = {
    "claude-code": {
        "config_paths": [
            Path.home() / ".claude" / "mcp.json",
            Path.cwd() / ".mcp.json",
        ],
        "schema_key": "mcpServers",
    },
    "claude-desktop": {
        "config_paths": _claude_desktop_config_paths(),
        "schema_key": "mcpServers",
    },
    "cursor": {
        "config_paths": [
            Path.home() / ".cursor" / "mcp.json",
            Path.cwd() / ".cursor" / "mcp.json",
        ],
        "schema_key": "mcpServers",
    },
}

def _claude_desktop_config_paths() -> list[Path]:
    if platform.system() == "Darwin":
        return [Path.home() / "Library/Application Support/Claude/claude_desktop_config.json"]
    if platform.system() == "Windows":
        return [Path.home() / "AppData/Roaming/Claude/claude_desktop_config.json"]
    return [Path.home() / ".config/Claude/claude_desktop_config.json"]

def init_command(ide: str, dry_run: bool, uninstall: bool):
    require_pro_license()  # ← Pro gate
    profile = IDE_PROFILES[ide]
    target = _resolve_target_path(profile)
    backup = _backup(target)
    config = _load_or_init(target)
    _merge_bobrain_entry(config, profile["schema_key"], uninstall=uninstall)
    if dry_run:
        print(json.dumps(config, indent=2))
        return
    _atomic_write(target, config)
    _print_restart_notice(ide)
```

bobrain エントリのテンプレ:

```json
{
  "mcpServers": {
    "bobrain": {
      "command": "uvx",
      "args": ["--from", "bobrain", "bobrain", "serve"],
      "env": {
        "BOBRAIN_DATA_DIR": "~/.bobrain"
      }
    }
  }
}
```

## 価格設計との接続

- **$49 LTD（Lifetime）**: Show HN ローンチ同日 Polar.sh で投入
- **30 日後の判断**: memory `bobrain_pypi_launch.md` の go/no-go ライン（500★ / W1 15% / Discord 100 / Setup 80%）到達なら月額 $10-15 の追加プラン検討
- ターゲット: 「mcp.json を毎回手で書きたくない」開発者。30 分 × 数 IDE × 数 project の試行錯誤コストを $49 で買う

## オープン論点

- ライセンス検証はオフライン重視で OK か（個人開発者は社内 proxy 環境で困ることもある）
- Cursor 用は project 単位の `.cursor/mcp.json` も書くべきか（user 単位だけで足りるか）
- `bobrain init --ide=all` で IDE が見つからない時のフォールバック挙動（silent skip / error / prompt）

## 関連

- DR raw: `Documents/マネタイズ/pages/sources/ローカルファースト RAG MCP 市場分析と価格戦略 2026-04-29.md`
- 価格戦略: memory `bobrain_pypi_launch.md` セクション 7
- 決済選定: memory `payment_mor_provider_split.md`（Polar.sh 単独）
