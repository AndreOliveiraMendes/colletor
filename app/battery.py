from datetime import datetime

from config import BASE


def read(path):
    try:
        with open(path, "r") as f:
            return f.read().strip()
    except Exception:
        return None

def get_power():
    return {
        "timestamp": datetime.now().isoformat(),
        "ac_online": read(f"{BASE}/AC/online") == "1",
        "status": read(f"{BASE}/BAT0/status"),
        "capacity": int(read(f"{BASE}/BAT0/capacity") or 0),
    }
