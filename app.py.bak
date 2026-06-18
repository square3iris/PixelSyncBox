from pixel_sync.adb import ADB
from pixel_sync.scanner import Scanner
from pixel_sync.sync import Sync


def main():

    ADB.devices()

    print()

    print("DCIM")
    print("-" * 60)

    for name in ADB.list_dir("/sdcard/DCIM"):
        print(name)

    print("=" * 60)

    scanner = Scanner()
    scanner.scan()

    sync = Sync()
    sync.upload_all()


if __name__ == "__main__":
    main()