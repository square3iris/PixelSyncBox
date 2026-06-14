from pixel_sync.db import Database
from pixel_sync.uploader import Uploader


class Sync:

    def __init__(self):

        self.db = Database()
        self.uploader = Uploader(self.db)

    def get_upload_list(self):

        return self.db.get_new_files()

    def upload_all(self):

        files = self.get_upload_list()

        self.uploader.upload_files(files)

        self.db.close()