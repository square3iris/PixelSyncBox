# ============================================
# FILE: pixel_sync/logger.py
# VERSION: 1.1.0
# UPDATED: 2026-06-21
# ============================================

from datetime import datetime
from pathlib import Path


class Logger:

    LOG_DIR = Path("logs")

    @classmethod
    def _write(cls, level, message):

        now = datetime.now()

        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        line = f"[{timestamp}] {level:<7} {message}"

        print(line)

        cls.LOG_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        logfile = (
            cls.LOG_DIR
            / f"{now:%Y-%m-%d}.log"
        )

        with open(
            logfile,
            "a",
            encoding="utf-8",
        ) as f:

            f.write(line + "\n")

    @classmethod
    def info(cls, message):

        cls._write("INFO", message)

    @classmethod
    def success(cls, message):

        cls._write("SUCCESS", message)

    @classmethod
    def warning(cls, message):

        cls._write("WARNING", message)

    @classmethod
    def error(cls, message):

        cls._write("ERROR", message)