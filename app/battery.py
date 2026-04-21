import os
from datetime import datetime

from config import HWMON_PATH


def read(path):
    try:
        with open(path) as f:
            return f.read().strip()
    except:
        return None

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


def get_power():
    ac_path, bat_path = find_power_devices()

    return {
        "timestamp": datetime.now().isoformat(),
        "ac_online": read(f"{ac_path}/online") == "1" if ac_path else None,
        "status": read(f"{bat_path}/status") if bat_path else None,
        "capacity": int(read(f"{bat_path}/capacity") or 0) if bat_path else None,
    }