import requests

from config import SERVER


def send_to_api(data):
    if not SERVER:
        return
    try:
        requests.post(SERVER, json=data, timeout=2)
    except requests.RequestException:
        pass