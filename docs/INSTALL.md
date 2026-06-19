# Pixel Sync Box インストールガイド

Version 1.4.0

---

# 必要なもの

- macOS
- Python 3.9以上
- Android Platform Tools (ADB)
- Google Pixel
- Google Photos

---

# 1. リポジトリ取得

```bash
git clone https://github.com/xxxxx/PixelSyncBox.git

cd PixelSyncBox
```

---

# 2. Python環境

推奨

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# 3. ADB確認

```bash
adb version
```

表示されればOK

---

# 4. Pixel設定

開発者オプション

✓ USBデバッグ

Google Photos

✓ バックアップON

---

# 5. USB接続

```bash
adb devices
```

例

```
FA68R0309241 device
```

---

# 6. settings.py を編集

編集するのはこのファイルだけです。

```python
PHOTO_DIR

DB_FILE

PIXEL_CAMERA_DIR

UPLOAD_THREADS
```

---

# 7. 初回スキャン

```bash
python3 app.py
```

データベースが作成されます。

---

# インストール完了