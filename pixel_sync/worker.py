from pathlib import Path

from pixel_sync.pixel import Pixel


class UploadWorker:

    def __init__(self, db):

        self.db = db
        self.pixel = Pixel()

    def upload(self, file_path, pixel_files):

        filename = Path(file_path).name

        if filename in pixel_files:
            return ("SKIP", file_path, filename)

        ok = self.pixel.upload(
            file_path,
            filename,
        )

        if ok:
            return ("SUCCESS", file_path, filename)

        return ("FAILED", file_path, filename)