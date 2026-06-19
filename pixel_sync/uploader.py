# ============================================
# FILE: pixel_sync/uploader.py
# VERSION: 1.1.0
# UPDATED: 2026-06-19
# ============================================

from concurrent.futures import ThreadPoolExecutor

from pixel_sync.config import UPLOAD_THREADS, COMMIT_INTERVAL
from pixel_sync.db import Database
from pixel_sync.worker import UploadWorker


class Uploader:

    def __init__(self, db: Database):

        self.db = db
        self.worker = UploadWorker()

    def upload_files(self, files):

        if not files:

            print("アップロードが必要なファイルはありません。")
            return

        pixel_files = self.worker.camera_files()

        uploaded_files = []

        total = len(files)

        success = 0
        skipped = 0
        failed = 0

        print()
        print("=" * 60)
        print("アップロード処理中")
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
                    uploaded_files.append(filename)
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
        print("アップロード完了")
        print("=" * 60)
        print(f"成功     : {success:,}")
        print(f"スキップ : {skipped:,}")
        print(f"失敗     : {failed:,}")

        if not uploaded_files:
            return

        print()
        print("=" * 60)
        print("Googleフォトのバックアップ待機")
        print("=" * 60)

        if self.worker.wait_backup_complete():

            self.worker.delete_uploaded_files(uploaded_files)

        else:

            print()
            print("=" * 60)
            print("Delete Skipped")
            print("=" * 60)
            print("Googleフォトのバックアップ完了を確認できなかったため削除を中止しました。")