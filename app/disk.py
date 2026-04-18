import re
import subprocess

def get_real_disks():
    result = subprocess.run(
        ["lsblk", "-dn", "-o", "NAME,TYPE"],
        capture_output=True,
        text=True
    )

    disks = []
    for line in result.stdout.splitlines():
        name, dtype = line.split()
        if dtype == "disk":
            disks.append(f"/dev/{name}")

    return disks

def get_disk_temp(disk="/dev/sda"):
    result = subprocess.run(
        ["smartctl", "-A", disk],
        capture_output=True,
        text=True
    )

    match = re.search(r"Temperature.*?(\d+)", result.stdout)
    if match:
        return int(match.group(1))
    
    return None

def get_all_disk_temps():
    disks = get_real_disks()
    temps = {}

    for d in disks:
        temp = get_disk_temp(d)
        if temp is not None:
            temps[d] = temp
        else:
            temps[d] = "???"
    return temps