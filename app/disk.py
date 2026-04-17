import subprocess


def get_disk_temp(disk):
    result = subprocess.run(
        ["smartctl", "-A", disk],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if "Temperature_Celsius" in line:
            return int(line.split()[9])

    return None