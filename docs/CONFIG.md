# settings.py

ユーザーが編集するのはこのファイルだけです。

## PHOTO_DIR

NAS写真フォルダ

例

```python
PHOTO_DIR="/Volumes/NAS/Photos"
```

---

## DB_FILE

SQLite保存場所

---

## PIXEL_CAMERA_DIR

通常

```
/sdcard/DCIM/Camera
```

変更不要

---

## UPLOAD_THREADS

並列数

推奨

```
4
```

---

## BACKUP_TIMEOUT

Google Photos待機時間

デフォルト

```
900秒
```