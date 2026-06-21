# CHANGELOG

## v1.4.0 (2026-06-21)

### Added

- ログファイル出力機能を追加
- `logs/` ディレクトリへ自動保存
- Ctrl+C による安全終了処理を追加
- SQLite の安全終了処理を追加
- ADB 自動再接続機能を追加
- ADB `push()` 自動再試行を追加
- ADB `shell()` 自動再試行を追加
- 多言語対応基盤 (`i18n`) を追加
- 日本語言語ファイル (`lang/ja.py`) を追加
- 英語言語ファイル (`lang/en.py`) を追加

### Changed

- アップロード成功時の状態を `DONE` から `UPLOADED` に変更
- Googleフォト完了後に `DONE` へ変更する方式へ修正
- 再開時に `UPLOADED` 状態も対象に変更
- プロジェクト構成を整理
- ドキュメント構成を整理
- テストデータを `tests/` 配下へ移動

### Fixed

- アプリ強制終了時に DB が閉じない問題を修正
- ADB 切断時に処理が即失敗する問題を修正
- Googleフォト完了前に `DONE` になる問題を修正

### Verified

正常動作を確認

- ログ出力
- Ctrl+C 安全終了
- DB close
- ADB 自動再接続
- ADB push 再試行
- ADB shell 再試行
- UPLOADED 状態管理
- DONE 状態管理
- py_compile 構文チェック

---

## v1.3.0 (2026-06-18)

### Added

- `prepare_ui()` を追加し、UI取得前処理を共通化
- `KEYCODE_WAKEUP` による安定した画面復帰
- ロック解除処理を共通化
- Googleフォト自動起動処理を追加
- `debug_print()` でも自動的に画面準備を行うよう改善
- バックアップ待機中（`backing_up`）判定を追加
- チュートリアル画面（`tutorial`）判定を追加
- ロック画面（`lock_screen`）判定を追加
- UI文字列取得処理を整理
- GoogleフォトUI解析の安定化

### Changed

- `get_backup_status()` を `prepare_ui()` ベースへ変更
- UI取得フローを統一
- XML解析処理を整理
- 判定ロジックを関数ごとに分離し保守性を向上

### Fixed

- `KEYCODE_POWER` では画面復帰が不安定だったため `KEYCODE_WAKEUP` に変更
- ロック画面取得による `unknown` 判定を改善
- Googleフォト起動タイミングを調整
- `debug_print()` と `get_backup_status()` の動作差異を解消

### Verified

正常動作を確認

- Googleフォト起動
- 画面復帰
- ロック解除
- UI取得
- XML解析
- `complete` 判定
- `backing_up` 判定
- `tutorial` 判定
- `lock_screen` 判定

---

## v1.2.0 (2026-06-18)

### Added

- `prepare_ui()` の初版実装
- GoogleフォトUI取得機能
- `KEYCODE_WAKEUP` 採用
- `debug_print()` 追加

### Verified

- Googleフォト起動成功
- UI取得成功
- `complete` 判定成功

---

## v1.1.0

### Completed

- Scanner 完成
- Database 完成
- Queue 管理完成
- Uploader 完成
- GoogleフォトUI解析開始
