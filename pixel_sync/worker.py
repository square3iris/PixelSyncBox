# ============================================
# FILE: pixel_sync/worker.py
# VERSION: 1.4.0
# UPDATED: 2026-06-18
# ============================================

import time
from pathlib import Path

from pixel_sync.pixel import Pixel
from pixel_sync.config import MAX_RETRY, RETRY_WAIT
from pixel_sync.settings import (
    BACKUP_TIMEOUT,
    BACKUP_STALLED_LIMIT,
)

from pixel_sync.ui import (
    get_backup_status,
    prepare_ui,
)
from pixel_sync.logger import Logger
from pixel_sync.i18n import tr


class UploadWorker:

    def __init__(self):

        self.pixel = Pixel()

    def camera_files(self):

        return self.pixel.camera_files()

    def upload(self, file_path, pixel_files):

        filename = Path(file_path).name

        if filename in pixel_files:
            return (
                "SKIP",
                file_path,
                filename,
            )

        for _ in range(MAX_RETRY):

            ok = self.pixel.upload(
                file_path,
                filename,
            )

            if ok:

                pixel_files.add(filename)

                return (
                    "SUCCESS",
                    file_path,
                    filename,
                )

            time.sleep(RETRY_WAIT)

        return (
            "FAILED",
            file_path,
            filename,
        )

    def wait_backup_complete(
        self,
        interval=10,
        timeout=3600,
    ):
        """
        Googleフォトのバックアップ完了を待機する
        """

        print()
        print("=" * 60)
        print(tr("backup.waiting"))
        print("=" * 60)

        start = time.time()

        unknown_count = 0
        backing_up_count = 0

        while True:

            status = get_backup_status()

            if status == "unknown":

                unknown_count += 1

                if unknown_count >= 5:

                    Logger.warning("Google Photos Recovery")

                    prepare_ui()

                    unknown_count = 0

            else:

                unknown_count = 0

            if status == "backing_up":

                backing_up_count += 1

                if backing_up_count >= BACKUP_STALLED_LIMIT:

                    Logger.warning(
                        "Google Photos Backup Stalled"
                    )

                    prepare_ui()

                    backing_up_count = 0

            else:

                backing_up_count = 0

            print(f"Status : {status}")

            if status == "complete":

                print(tr("backup.complete"))

                return True

            if time.time() - start > timeout:

                print(tr("backup.timeout"))

                return False

            time.sleep(interval)
    def delete_uploaded_files(self, filenames):
        """
        アップロード済みファイルをPixelから削除する
        """

        print()
        print("=" * 60)
        print(tr("delete.start"))
        print("=" * 60)

        deleted = 0

        for filename in filenames:

            if self.pixel.delete_file(filename):

                print(f"DELETE : {filename}")
                deleted += 1

            else:

                print(f"FAILED : {filename}")

        print()
        print(f"Deleted : {deleted}/{len(filenames)}")

        return deleted

