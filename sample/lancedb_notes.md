# LanceDB メモ

LanceDB は単一ファイルで動く組み込み型ベクトル DB。Rust 実装で TypeScript / Python の両方から使える。

## 特徴

- サーバー不要（embedded）、ファイル単位で portable
- Apache Arrow / Parquet 互換
- 全文検索 + ベクトル検索 + フィルタが同時に使える

## 代替候補との比較

- Chroma: Python エコシステムで人気、組み込み可能だが Rust ベースではない
- Qdrant: サーバー型が主、組み込みモードもあり、パフォーマンス高
- pgvector: PostgreSQL 必要、overkill になりがち
