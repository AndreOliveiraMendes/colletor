from datetime import datetime

import requests

from app.log import log_data
from config import SERVER


def send_to_api(data):
    try:
        requests.post(SERVER, json=data, timeout=2)
    except requests.RequestException as e:
        log_data(
            {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "type": e.__class__.__name__,
                "server": SERVER,
                "payload": data,
            },
            "error_log"
        )