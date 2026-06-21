# ============================================
# FILE: pixel_sync/sync.py
# VERSION: 1.1.0
# UPDATED: 2026-06-18
# ============================================
from pixel_sync.db import Database
from pixel_sync.uploader import Uploader


class Sync:

    def __init__(self):

        self.db = Database()
        self.uploader = Uploader(self.db)

    def get_upload_list(self):

        return self.db.get_new_files()

    def upload_all(self):

        try:

            files = self.get_upload_list()

            # TEST MODE
            files = files[:10]

            self.uploader.upload_files(files)

        finally:

            self.db.close()
    def run(self):

        self.upload_all()
