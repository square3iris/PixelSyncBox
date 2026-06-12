import os
import time
from pathlib import Path

from pixel_sync.config import PHOTO_DIR, SUPPORTED_EXTENSIONS
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
        print("Pixel Sync Box Scanner")
        print("=" * 60)
        print(f"Target : {PHOTO_DIR}")
        print()

        self._scan_dir(PHOTO_DIR)

        self.db.commit()

        elapsed = time.time() - self.start_time

        print()
        print("=" * 60)
        print("Finished")
        print("=" * 60)

        print(f"Images   : {self.image_files:,}")
        print(f"Videos   : {self.video_files:,}")
        print(f"Total    : {self.total_files:,}")
        print()
        print(f"New      : {self.new_files:,}")
        print(f"Updated  : {self.updated_files:,}")
        print(f"Skipped  : {self.skipped_files:,}")
        print()
        print(f"Database : {self.db.count():,} records")
        print(f"Elapsed  : {elapsed:.1f} sec")

        if elapsed > 0:
            print(f"Speed    : {self.total_files / elapsed:.1f} files/sec")

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
                        self.db.update_status(media.path, "NEW")
                        self.new_files += 1

                    else:

                        old_size, old_mtime = record

                        if (
                            old_size != media.size
                            or old_mtime != media.mtime
                        ):

                            self.db.update_file(media)
                            self.db.update_status(media.path, "UPDATED")
                            self.updated_files += 1

                        else:

                            self.db.update_status(media.path, "SKIP")
                            self.skipped_files += 1

                    if self.total_files % 1000 == 0:

                        elapsed = time.time() - self.start_time

                        speed = (
                            self.total_files / elapsed
                            if elapsed > 0
                            else 0
                        )

                        print(
                            f"{self.total_files:>8,} files | "
                            f"{speed:>8.1f} files/sec | "
                            f"New:{self.new_files:>6} "
                            f"Upd:{self.updated_files:>6} "
                            f"Skip:{self.skipped_files:>6}"
                        )

        except PermissionError:

            print(f"Skip : {folder}")