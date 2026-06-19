# ============================================
# FILE: pixel_sync/ui.py
# VERSION: 1.3.0
# UPDATED: 2026-06-18
# ============================================

import subprocess
import time
import xml.etree.ElementTree as ET

UI_XML = "ui.xml"


def adb(*args):
    subprocess.run(
        ["adb", *args],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def wakeup():
    adb("shell", "input", "keyevent", "KEYCODE_WAKEUP")
    time.sleep(1)


def unlock():
    adb("shell", "input", "swipe", "500", "1800", "500", "300")
    time.sleep(1)


def launch_photos():
    adb(
        "shell",
        "monkey",
        "-p",
        "com.google.android.apps.photos",
        "1",
    )
    time.sleep(3)


def prepare_ui():
    """
    GoogleフォトのUI取得ができる状態まで持っていく
    """

    wakeup()
    unlock()
    launch_photos()


def dump_ui():
    adb("shell", "uiautomator", "dump", "/sdcard/ui.xml")
    adb("pull", "/sdcard/ui.xml", UI_XML)


def read_texts():
    try:
        tree = ET.parse(UI_XML)
        root = tree.getroot()

        texts = []

        for node in root.iter():

            text = node.attrib.get("text", "").strip()
            if text:
                texts.append(text)

            desc = node.attrib.get("content-desc", "").strip()
            if desc:
                texts.append(desc)

        return texts

    except Exception:
        return []


def debug_print():
    prepare_ui()
    dump_ui()

    print("===== 取得したUIテキスト一覧 =====")

    for t in read_texts():
        print(t)


def is_lock_screen(texts):

    keywords = [
        "USBデバッグ",
        "充電完了",
        "Android システム",
        "サイレント モード",
    ]

    hit = 0

    for k in keywords:
        if any(k in t for t in texts):
            hit += 1

    return hit >= 2


def is_tutorial(texts):

    keywords = [
        "新たな検索",
        "検索＆クリエイト",
        "試してみる",
    ]

    return any(
        any(k in t for k in keywords)
        for t in texts
    )


def is_complete(texts):

    keywords = [
        "バックアップ完了",
        "バックアップが完了",
    ]

    return any(
        any(k in t for k in keywords)
        for t in texts
    )


def is_backing_up(texts):

    keywords = [
        "バックアップ中",
        "バックアップしています",
        "アップロード中",
        "残り",
        "あと",
    ]

    return any(
        any(k in t for k in keywords)
        for t in texts
    )


def is_waiting(texts):

    keywords = [
        "アップロードを待機しています",
        "Wi-Fi を待機しています",
        "Wi-Fiに接続されるのを待っています",
        "充電を待機しています",
    ]

    return any(
        any(k in t for k in keywords)
        for t in texts
    )


def get_backup_status():

    prepare_ui()

    dump_ui()
    texts = read_texts()

    if is_lock_screen(texts):
        return "lock_screen"

    if is_tutorial(texts):
        return "tutorial"

    if is_waiting(texts):
        return "waiting"

    if is_complete(texts):
        return "complete"

    if is_backing_up(texts):
        return "backing_up"

    return "unknown"