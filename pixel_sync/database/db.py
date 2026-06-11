import sqlite3
from pixel_sync.config import DB_FILE


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS files(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            path TEXT UNIQUE,

            filename TEXT,

            size INTEGER,

            sha256 TEXT,

            mtime REAL,

            status TEXT,

            retry INTEGER DEFAULT 0,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        );
        """)

        self.conn.commit()