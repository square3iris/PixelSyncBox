# ============================================
# FILE: pixel_sync/uploader.py
# VERSION: 1.0.1
# CHANGES: Add development header
# ============================================
from concurrent.futures import ThreadPoolExecutor, as_completed
from pixel_sync.config import UPLOAD_THREADS, COMMIT_INTERVAL

from pixel_sync.db import Database
from pixel_sync.worker import UploadWorker


class Uploader:

    def __init__(self, db: Database):

        self.db = db
        self.worker = UploadWorker()

    def upload_files(self, files):

        if not files:

            print("Nothing to upload.")
            return

        pixel_files = self.worker.camera_files()

        total = len(files)

        success = 0
        skipped = 0
        failed = 0

        print()
        print("=" * 60)
        print("Uploading")
        print("=" * 60)

        with ThreadPoolExecutor(max_workers=UPLOAD_THREADS) as executor:

            futures = [
                executor.submit(
                    self.worker.upload,
                    file_path,
                    pixel_files,
                )
                for file_path in files
            ]

            for index, future in enumerate(futures, start=1):

                result, file_path, filename = future.result()

                if result == "SUCCESS":

                    self.db.update_status(file_path, "DONE")
                    pixel_files.add(filename)
                    success += 1

                elif result == "SKIP":

                    self.db.update_status(file_path, "DONE")
                    skipped += 1

                else:

                    failed += 1

                if index % COMMIT_INTERVAL == 0:
                    self.db.commit()

                print(
                    f"[{index:,}/{total:,}] "
                    f"{result:<7} {filename}"
                )

        self.db.commit()

        print()
        print("=" * 60)
        print("Finished Upload")
        print("=" * 60)
        print(f"Uploaded : {success:,}")
        print(f"Skipped  : {skipped:,}")
        print(f"Failed   : {failed:,}")