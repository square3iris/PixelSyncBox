# ============================================
# FILE: pixel_sync/config.py
# VERSION: 1.1.0
# UPDATED: 2026-06-15
# ============================================

from pathlib import Path

# ===== NAS =====

PHOTO_DIR = Path("/Volumes/HFS8TB/Share/Data/写真_映像")

# ===== Database =====

DB_FILE = Path("database/pixel_sync.db")

# ===== Pixel =====

PIXEL_UPLOAD_DIR = "/sdcard/DCIM/PixelSyncBox"

# ===== Upload =====

BATCH_SIZE_GB = 20

BATCH_SIZE = BATCH_SIZE_GB * 1024 * 1024 * 1024

UPLOAD_THREADS = 2
MAX_RETRY = 3
RETRY_WAIT = 1
COMMIT_INTERVAL = 20

# ===== Scan =====

SUPPORTED_EXTENSIONS = {

    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",

    ".heic",
    ".heif",

    ".mp4",
    ".mov",
    ".m4v",
    ".avi",
    ".mts",
    ".m2ts",
    ".mkv"

}