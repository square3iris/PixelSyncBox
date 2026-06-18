# ============================================
# FILE: pixel_sync/logger.py
# VERSION: 1.0.0
# UPDATED: 2026-06-15
# ============================================

from datetime import datetime


class Logger:

    @staticmethod
    def _write(level, message):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{now}] {level:<7} {message}")

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