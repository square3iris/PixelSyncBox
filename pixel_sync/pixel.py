# ============================================
# FILE: pixel_sync/pixel.py
# VERSION: 1.1.0
# CHANGES: Add camera file cache support
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