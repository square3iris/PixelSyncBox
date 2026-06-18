# ============================================
# FILE: pixel_sync/ui.py
# VERSION: 2.0.0
# UPDATED: 2026-06-17
# DESCRIPTION: Stable UI parser for Pixel Photos backup detection
# ============================================

import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


UI_PATH = Path("ui.xml")


# ------------------------------------------------
# ADB UI dump
# ------------------------------------------------
def dump_ui():
    try:
        subprocess.run(
            ["adb", "shell", "uiautomator", "dump", "/sdcard/ui.xml"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

        subprocess.run(
            ["adb", "pull", "/sdcard/ui.xml", str(UI_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

        return True
    except Exception:
        return False


# ------------------------------------------------
# XML parse
# ------------------------------------------------
def parse_ui_texts():
    if not UI_PATH.exists():
        return []

    try:
        tree = ET.parse(UI_PATH)
        root = tree.getroot()

        texts = []
        for node in root.iter("node"):
            text = node.attrib.get("text", "")
            if text:
                texts.append(text)

        return texts

    except Exception:
        return []


# ------------------------------------------------
# debug
# ------------------------------------------------
def debug_print():
    dump_ui()
    texts = parse_ui_texts()

    print("===== UI TEXTS =====")
    for t in texts:
        print(t)


# ------------------------------------------------
# core logic
# ------------------------------------------------
def get_backup_status():
    dump_ui()
    texts = parse_ui_texts()

    text_blob = " ".join(texts)

    # =================================================
    # 1. LOCK SCREEN FILTER（最重要）
    # =================================================
    lock_indicators = [
        "充電完了",
        "サイレント モード",
        "スワイプして",
        "ロック解除",
        "通知"
    ]

    if any(k in text_blob for k in lock_indicators):
        # ロック画面の可能性が高い
        return "lock_screen"

    # =================================================
    # 2. GOOGLE PHOTOS DETECTION
    # =================================================
    photos_indicators = [
        "フォト",
        "Google Photos",
        "ライブラリ",
        "コレクション",
        "作成"
    ]

    if not any(k in text_blob for k in photos_indicators):
        return "not_in_photos"

    # =================================================
    # 3. BACKUP STATE DETECTION
    # =================================================
    backup_running_keywords = [
        "バックアップ中",
        "バックアップしています",
        "準備しています",
        "アップロード中"
    ]

    backup_done_keywords = [
        "バックアップ完了",
        "完了しました",
        "すべてバックアップ済み"
    ]

    backup_error_keywords = [
        "エラー",
        "一時停止",
        "Wi-Fi待機"
    ]

    if any(k in text_blob for k in backup_running_keywords):
        return "backing_up"

    if any(k in text_blob for k in backup_done_keywords):
        return "complete"

    if any(k in text_blob for k in backup_error_keywords):
        return "paused_or_error"

    # =================================================
    # 4. FALLBACK
    # =================================================
    return "unknown"


# ------------------------------------------------
# helper for CLI test
# ------------------------------------------------
if __name__ == "__main__":
    print(get_backup_status())