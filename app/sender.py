from datetime import datetime

import requests

from app.log import log_data
from config import SERVER


def send_to_api(data):
    try:
        resp = requests.post(SERVER, json=data, timeout=2)

        # tenta parsear JSON, mas sem quebrar se não vier
        try:
            resp_json = resp.json()
        except ValueError:
            resp_json = None

        if resp.status_code >= 400 or resp.status_code == 207:
            log_data(
                {
                    "timestamp": datetime.now().isoformat(),
                    "error": "bad response",
                    "status_code": resp.status_code,
                    "response": resp_json,
                    "raw_response": resp.text[:500],  # evita log gigante
                    "server": SERVER,
                    "payload": data,
                },
                "error_log"
            )

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