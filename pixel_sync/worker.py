# ============================================
# FILE: pixel_sync/worker.py
# VERSION: 1.2.0
# UPDATED: 2026-06-16
# ============================================

import time
from pathlib import Path

from pixel_sync.pixel import Pixel
from pixel_sync.config import MAX_RETRY, RETRY_WAIT


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