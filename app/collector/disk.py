import subprocess
import json

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

def get_disk_info(disk):
    cmd = ["sudo", "smartctl", "-a", "--json", disk]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if not result.stdout:
        return None

    try:
        data = json.loads(result.stdout)
    except:
        return None

    return data

def get_disk():
    out = []

    for disk in get_real_disks():
        data = get_disk_info(disk)

        if not data:
            continue

        temp = data.get("temperature", {}).get("current")

        out.append({
            "type": "temperature",
            "device": "disk",
            "source": "local",
            "name": disk.split("/")[-1],
            "value": temp,
            "meta": {
                "path": disk,
                "model": data.get("model_name"),
                "health": data.get("smart_status", {}).get("passed"),
                "power_on_hours": data.get("power_on_time", {}).get("hours"),
            }
        })

    return out