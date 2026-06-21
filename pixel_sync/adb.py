# ============================================
# FILE: pixel_sync/adb.py
# VERSION: 1.2.0
# UPDATED: 2026-06-18
# ============================================

import subprocess
import time

from pixel_sync.logger import Logger


class ADB:

    @staticmethod
    def devices():

        print("=" * 60)
        print("ADB 接続デバイス一覧")
        print("=" * 60)

        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True
        )

        devices = []

        for line in result.stdout.splitlines()[1:]:

            line = line.strip()

            if not line:
                continue

            if "\tdevice" in line:

                serial = line.split()[0]
                devices.append(serial)
                print(serial)

        print()
        print(f"{len(devices)} 台のデバイスが接続されています。")

        return devices


    @staticmethod
    def has_device():

        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True
        )

        for line in result.stdout.splitlines()[1:]:

            if "\tdevice" in line:

                return True

        return False

    @staticmethod
    def list_dir(path):

        result = subprocess.run(
            ["adb", "shell", "ls", path],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return []

        return [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

    @staticmethod
    def push(local_path, remote_path):

        result = subprocess.run(
            [
                "adb",
                "push",
                str(local_path),
                remote_path,
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return True

        Logger.warning("ADB push failed")

        if not ADB.reconnect():
            return False

        result = subprocess.run(
            [
                "adb",
                "push",
                str(local_path),
                remote_path,
            ],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0

    @staticmethod
    def shell(*args):
        """
        adb shell を実行する
        """

        result = subprocess.run(
            [
                "adb",
                "shell",
                *map(str, args),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            return True

        Logger.warning("ADB shell failed")

        if not ADB.reconnect():
            return False

        result = subprocess.run(
            [
                "adb",
                "shell",
                *map(str, args),
            ],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0

    @staticmethod
    def reconnect(max_retry=30):

        for attempt in range(max_retry):

            if ADB.has_device():

                Logger.success("ADB reconnected")
                return True

            Logger.warning(
                f"ADB disconnected retry={attempt + 1}/{max_retry}"
            )

            time.sleep(2)

        Logger.error("ADB reconnect failed")
        return False

