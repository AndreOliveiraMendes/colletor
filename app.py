import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv('BASE')
SERVER = os.getenv('SERVER')
LOG = os.getenv('LOG')

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

def send_to_api(data):
    try:
        requests.post(SERVER, json=data, timeout=2)
    except requests.RequestException:
        pass  # evita travar script

def log_data(data):
    with open(LOG, "a") as f:  # append
        f.write(json.dumps(data) + "\n")

if __name__ == "__main__":
    data = get_power()

    if SERVER:
        send_to_api(data)

    log_data(data)
