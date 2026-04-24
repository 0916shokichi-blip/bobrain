# MCP (Model Context Protocol) の基礎

MCP は LLM と外部のデータ・ツールを繋ぐオープン標準。Anthropic が 2024 年 11 月に公開。
「AI のための USB-C」と呼ばれる。

## 3 つの機能カテゴリ

- **Tools**: LLM が呼び出せる関数
- **Resources**: LLM が参照できるデータ
- **Prompts**: 再利用可能なプロンプトテンプレート

## クライアント

Claude Desktop / Claude Code / Cursor / Windsurf / OpenAI Agents などが MCP に対応。
サーバー側を 1 つ作れば、全クライアントで同時に使えるのが特徴。
