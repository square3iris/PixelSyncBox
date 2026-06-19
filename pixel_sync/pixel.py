# ============================================
# FILE: pixel_sync/pixel.py
# VERSION: 1.2.0
# UPDATED: 2026-06-18
# ============================================

from pixel_sync.adb import ADB


class Pixel:

    CAMERA_DIR = "/sdcard/DCIM/Camera"
    BACKUP_DIR = "/sdcard/DCIM/Backup"

    def camera_files(self):

        return set(
            ADB.list_dir(self.CAMERA_DIR)
        )

    def upload(self, local_path, filename):

        remote = f"{self.CAMERA_DIR}/{filename}"

        return ADB.push(
            local_path,
            remote,
        )

    def delete_file(self, filename):
        """
        Pixel内のファイルを1件削除する
        """

        remote = f"{self.CAMERA_DIR}/{filename}"

        return ADB.shell(
            "rm",
            remote,
        )

    def delete_files(self, filenames):
        """
        Pixel内の複数ファイルを削除する
        """

        success = 0

        for filename in filenames:

            if self.delete_file(filename):
                success += 1

        return success