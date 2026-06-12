import subprocess


class ADB:

    @staticmethod
    def devices():

        print("=" * 60)
        print("ADB Devices")
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

        print(f"{len(devices)} device(s) connected.")

        return devices

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

        return subprocess.run(
            [
                "adb",
                "push",
                str(local_path),
                remote_path
            ]
        ).returncode == 0