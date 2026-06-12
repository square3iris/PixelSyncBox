import sqlite3
from pathlib import Path

from pixel_sync.config import DB_FILE


class Database:

    def __init__(self):

        Path(DB_FILE).parent.mkdir(parents=True, exist_ok=True)

        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            path TEXT UNIQUE,
            filename TEXT,
            extension TEXT,

            size INTEGER,
            mtime REAL,

            media_type TEXT,
            status TEXT,

            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """)

        self.conn.commit()

    def insert_file(self, media):

        self.cursor.execute("""
        INSERT OR IGNORE INTO files
        (
            path,
            filename,
            extension,
            size,
            mtime,
            media_type,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            str(media.path),
            media.filename,
            media.extension,
            media.size,
            media.mtime,
            media.media_type,
            "NEW"
        ))

    def exists(self, path):

        self.cursor.execute(
            "SELECT size, mtime FROM files WHERE path=?",
            (str(path),)
        )

        return self.cursor.fetchone()

    def update_file(self, media):

        self.cursor.execute("""
        UPDATE files
        SET
            filename=?,
            extension=?,
            size=?,
            mtime=?,
            media_type=?,
            updated_at=CURRENT_TIMESTAMP
        WHERE path=?
        """, (
            media.filename,
            media.extension,
            media.size,
            media.mtime,
            media.media_type,
            str(media.path)
        ))

    def update_status(self, path, status):

        self.cursor.execute("""
        UPDATE files
        SET
            status=?,
            updated_at=CURRENT_TIMESTAMP
        WHERE path=?
        """, (
            status,
            str(path)
        ))

    def count(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM files"
        )

        return self.cursor.fetchone()[0]

    def commit(self):

        self.conn.commit()

    def close(self):

        self.conn.close()