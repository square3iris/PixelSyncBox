# Decision

## ScannerはSKIPを書き込まない

変更のないファイルはDBを書き換えない。

理由

- NEW状態を維持できる
- Upload対象が消えない
- DB更新量削減
- 設計が単純になる

状態管理

NEW
UPDATED
DONE
FAILED（予定）

SKIPは画面表示専用。