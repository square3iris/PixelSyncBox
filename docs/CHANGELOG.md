## v1.3.0 (2026-06-19)

### Added
- Google Photos のバックアップ状態自動判定機能
- Pixel の画面起動・ロック解除処理
- Google Photos 自動起動
- Google Photos UI解析（uiautomator）
- ロック画面検出
- Google Photos チュートリアル画面検出
- バックアップ待機処理 (`wait_backup_complete()`)
- バックアップ完了後の Pixel ファイル自動削除

### Changed
- Scanner が既存ファイルを `SKIP` に更新しない設計へ変更
- DBの `NEW` 状態を維持するよう改善
- Upload完了後に Google Photos のバックアップ完了を待機してから削除するフローへ変更
- UI解析モジュール (`ui.py`) を v1.3.0 として全面改善
- Google Photos の「待機中」「バックアップ中」「完了」を判定可能に改善

### Fixed
- ロック画面誤判定
- Google Photos 起動直後のUI取得失敗
- バックアップ完了前に削除される可能性を解消
- Scanner が NEW を消してしまう問題