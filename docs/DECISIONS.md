# Architecture Decisions

## 2026-06-11

### Scannerはos.scandirを採用

理由

Path.rglobより高速。

約10万ファイル以上では性能差が大きい。

---

### SQLiteを中心設計にする

Scanner

↓

SQLite

↓

Uploader

↓

GUI

すべてSQLite経由で状態管理する。