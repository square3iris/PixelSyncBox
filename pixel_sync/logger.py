# ============================================
# FILE: pixel_sync/logger.py
# VERSION: 1.0.1
# UPDATED: 2026-06-18
# ============================================

from datetime import datetime


class Logger:

    @staticmethod
    def _write(level, message):

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"[{now}] {level:<7} {message}")

    @classmethod
    def info(cls, message):

        cls._write("情報", message)

    @classmethod
    def success(cls, message):

        cls._write("成功", message)

    @classmethod
    def warning(cls, message):

        cls._write("警告", message)

    @classmethod
    def error(cls, message):

        cls._write("エラー", message)