# ============================================
# FILE: app.py
# VERSION: 1.1.0
# UPDATED: 2026-06-18
# ============================================
from pixel_sync.adb import ADB
from pixel_sync.scanner import Scanner
from pixel_sync.sync import Sync


def main():

    ADB.devices()

    print()

    print("Pixel 内部ストレージの状態 (/sdcard/DCIM)")
    print("-" * 60)

    for name in ADB.list_dir("/sdcard/DCIM"):
        print(name)

    print("=" * 60)

    scanner = Scanner()
    scanner.scan()

    Sync().run()


if __name__ == "__main__":
    main()
