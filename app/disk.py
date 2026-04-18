import re
import subprocess

def get_real_disks():
    result = subprocess.run(
        ["lsblk", "-dn", "-o", "NAME,TYPE,SIZE"],
        capture_output=True,
        text=True
    )

    disks = []
    for line in result.stdout.splitlines():
        name, dtype, size = line.split()

        if dtype == "disk" and size != "0B":
            disks.append(f"/dev/{name}")

    return disks

def get_disk_smart(disk):
    commands = [
        ["sudo", "smartctl", "-A", disk],              # direto
        ["sudo", "smartctl", "-A", "-d", "sat", disk], # USB
    ]

    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if "Temperature" in result.stdout:
            return result.stdout

    return None

def get_all_disk_temps():
    disks = get_real_disks()
    temps = {}

    for d in disks:
        temp = get_disk_smart(d)
        if temp is not None:
            temps[d] = temp
        else:
            temps[d] = "???"
    return temps