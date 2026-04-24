# RAG の概要

RAG (Retrieval-Augmented Generation) は、LLM に外部知識を注入する手法。
生成前に検索で関連文書を引き、プロンプトに文脈として埋め込む。

## ハイブリッド検索

キーワード検索 (BM25) とベクトル検索 (Embeddings) を組み合わせると精度が上がる。
結果統合には Reciprocal Rank Fusion (RRF) がよく使われる。

## チャンキング戦略

- 固定長: 実装が簡単だが、意味境界を壊しやすい
- heading aware: Markdown の見出しで分割
- AST aware: コードは tree-sitter で構文に沿って分割
