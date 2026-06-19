# ============================================
# FILE: pixel_sync/scanner.py
# VERSION: 1.1.0
# UPDATED: 2026-06-18
# ============================================
import os
import time
from pathlib import Path

from pixel_sync.settings import PHOTO_DIR
from pixel_sync.config import SUPPORTED_EXTENSIONS
from pixel_sync.media import MediaFile
from pixel_sync.db import Database


IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".heic",
    ".heif",
}


class Scanner:

    def __init__(self):

        self.db = Database()

        self.total_files = 0
        self.image_files = 0
        self.video_files = 0

        self.new_files = 0
        self.updated_files = 0
        self.skipped_files = 0

        self.start_time = 0

    def scan(self):

        self.start_time = time.time()

        print("=" * 60)
        print("Pixel Sync Box スキャナー")
        print("=" * 60)
        print(f"対象ディレクトリ : {PHOTO_DIR}")
        print()

        self._scan_dir(PHOTO_DIR)

        self.db.commit()

        elapsed = time.time() - self.start_time

        print()
        print("=" * 60)
        print("スキャン完了")
        print("=" * 60)

        print(f"画像ファイル : {self.image_files:,}")
        print(f"動画ファイル : {self.video_files:,}")
        print(f"合計ファイル : {self.total_files:,}")
        print()

        print(f"新規追加     : {self.new_files:,}")
        print(f"更新         : {self.updated_files:,}")
        print(f"スキップ     : {self.skipped_files:,}")
        print()

        print(f"データベース : {self.db.count():,} レコード")
        print(f"経過時間     : {elapsed:.1f} 秒")

        if elapsed > 0:
            print(f"処理速度     : {self.total_files / elapsed:.1f} ファイル/秒")

        self.db.close()

    def _scan_dir(self, folder: Path):

        try:

            with os.scandir(folder) as entries:

                for entry in entries:

                    if entry.name.startswith("."):
                        continue

                    if entry.is_dir(follow_symlinks=False):
                        self._scan_dir(Path(entry.path))
                        continue

                    ext = Path(entry.name).suffix.lower()

                    if ext not in SUPPORTED_EXTENSIONS:
                        continue

                    self.total_files += 1

                    if ext in IMAGE_EXTENSIONS:
                        self.image_files += 1
                        media_type = "IMAGE"
                    else:
                        self.video_files += 1
                        media_type = "VIDEO"

                    stat = entry.stat()

                    media = MediaFile(
                        path=Path(entry.path),
                        filename=entry.name,
                        extension=ext,
                        size=stat.st_size,
                        mtime=stat.st_mtime,
                        media_type=media_type,
                    )

                    record = self.db.exists(media.path)

                    if record is None:

                        self.db.insert_file(media)
                        self.new_files += 1

                    else:

                        old_size, old_mtime = record

                        if (
                            old_size != media.size
                            or old_mtime != media.mtime
                        ):

                            self.db.update_file(media)
                            self.updated_files += 1

                        else:

                            self.skipped_files += 1

                    if self.total_files % 1000 == 0:

                        elapsed = time.time() - self.start_time

                        speed = (
                            self.total_files / elapsed
                            if elapsed > 0
                            else 0
                        )

                        print(
                            f"{self.total_files:>8,} ファイル | "
                            f"{speed:>8.1f} ファイル/秒 | "
                            f"新規:{self.new_files:>6} "
                            f"更新:{self.updated_files:>6} "
                            f"スキップ:{self.skipped_files:>6}"
                        )

        except PermissionError:

            print(f"アクセス拒否のためスキップ : {folder}")