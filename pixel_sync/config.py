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