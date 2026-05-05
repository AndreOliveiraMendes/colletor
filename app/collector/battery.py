import os

from app.utils import read
from config import HWMON_PATH


def find_power_devices():
    ac_path = None
    bat_path = None

    for dev in os.listdir(HWMON_PATH):
        dev_path = os.path.join(HWMON_PATH, dev)
        dev_type = read(os.path.join(dev_path, "type"))

        if dev_type == "Mains":
            ac_path = dev_path
        elif dev_type == "Battery":
            bat_path = dev_path

    return ac_path, bat_path


def get_battery():
    ac_path, bat_path = find_power_devices()

    if not bat_path:
        return []

    def safe_int(path):
        val = read(path)
        return int(val) if val and val.isdigit() else None

    charge_full = safe_int(f"{bat_path}/charge_full")
    charge_full_design = safe_int(f"{bat_path}/charge_full_design")

    health = None
    if charge_full and charge_full_design:
        health = round((charge_full / charge_full_design) * 100, 2)

    data = {
        "ac_online": read(f"{ac_path}/online") == "1" if ac_path else None,
        "status": read(f"{bat_path}/status"),
        "capacity": safe_int(f"{bat_path}/capacity"),
        "health": health,
        "charge_now": safe_int(f"{bat_path}/charge_now"),
        "cycle_count": safe_int(f"{bat_path}/cycle_count"),
    }

    return [{
        "type": "battery",
        "source": "local",
        "device": "battery",
        "value": data["capacity"],
        "meta": data
    }]