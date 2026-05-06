import json
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

def extract_health(data):
    attrs = data.get("ata_smart_attributes", {}).get("table", [])

    def get_attr(name):
        for a in attrs:
            if a.get("name") == name:
                return a.get("raw", {}).get("value")
        return None

    return {
        "passed": data.get("smart_status", {}).get("passed"),
        "reallocated_sectors": get_attr("Reallocated_Sector_Ct"),
        "pending_sectors": get_attr("Current_Pending_Sector"),
        "offline_uncorrectable": get_attr("Offline_Uncorrectable"),
        "power_on_hours": data.get("power_on_time", {}).get("hours"),
        "temperature": data.get("temperature", {}).get("current"),
        "error_count": data.get("ata_smart_error_log", {}).get("summary", {}).get("count")
    }

def get_disk_temperature():
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

def get_disk_health():
    out = []

    for disk in get_real_disks():
        data = get_disk_info(disk)
        if not data:
            continue

        health = extract_health(data)

        out.append({
            "type": "health",
            "device": "disk",
            "source": "local",
            "name": disk.split("/")[-1],
            "value": 1 if health["passed"] else 0,
            "meta": {
                "path": disk,
                "model": data.get("model_name"),
                **health
            }
        })

    return out