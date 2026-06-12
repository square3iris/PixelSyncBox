from pixel_sync.db import Database


class Sync:

    def __init__(self):

        self.db = Database()

    def get_upload_list(self):

        self.db.cursor.execute("""
            SELECT
                path,
                filename
            FROM files
            WHERE status='NEW'
            ORDER BY id
        """)

        return self.db.cursor.fetchall()