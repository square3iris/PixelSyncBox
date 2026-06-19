# ============================================
# FILE: pixel_sync/worker.py
# VERSION: 1.4.0
# UPDATED: 2026-06-18
# ============================================

import time
from pathlib import Path

from pixel_sync.pixel import Pixel
from pixel_sync.config import MAX_RETRY, RETRY_WAIT
from pixel_sync.ui import get_backup_status


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
        print("Waiting Google Photos Backup")
        print("=" * 60)

        start = time.time()

        while True:

            status = get_backup_status()

            print(f"Status : {status}")

            if status == "complete":

                print("Backup Complete")

                return True

            if time.time() - start > timeout:

                print("Backup Timeout")

                return False

            time.sleep(interval)
    def delete_uploaded_files(self, filenames):
        """
        アップロード済みファイルをPixelから削除する
        """

        print()
        print("=" * 60)
        print("Deleting Uploaded Files")
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

