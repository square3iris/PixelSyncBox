from pathlib import Path

from pixel_sync.adb import ADB


class Uploader:

    def __init__(self, db):

        self.db = db

    def upload_file(self, file_path, pixel_files):

        filename = Path(file_path).name

        # 既にPixelに存在するなら転送しない
        if filename in pixel_files:

            self.db.update_status(file_path, "DONE")

            return (
                "SKIP",
                filename,
            )

        remote_path = f"/sdcard/DCIM/Camera/{filename}"

        ok = ADB.push(
            file_path,
            remote_path,
        )

        if ok:

            self.db.update_status(
                file_path,
                "DONE",
            )

            pixel_files.add(filename)

            return (
                "SUCCESS",
                filename,
            )

        return (
            "FAILED",
            filename,
        )

    def upload_files(self, files):

        if not files:

            print("Nothing to upload.")
            return

        pixel_files = set(
            ADB.list_dir("/sdcard/DCIM/Camera")
        )

        total = len(files)

        success = 0
        skipped = 0
        failed = 0

        print()
        print("=" * 60)
        print("Uploading")
        print("=" * 60)

        for index, file_path in enumerate(files, start=1):

            result, filename = self.upload_file(
                file_path,
                pixel_files,
            )

            if result == "SUCCESS":
                success += 1

            elif result == "SKIP":
                skipped += 1

            else:
                failed += 1

            if index % 20 == 0:
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