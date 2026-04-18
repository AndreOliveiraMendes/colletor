from datetime import datetime

from app.cpu import get_cpu_temps
from app.disk import get_all_disk_temps
from app.log import log_data
from app.sender import send_to_api
from config import HOSTIP, HOSTNAME


def build_send_data(device_type, name, value, meta=None):
    data = {
        "type": "temperature",
        "source": "local",
        "host_name": HOSTNAME,
        "host_ip": HOSTIP,
        "device_type": device_type,
        "name": name,
        "value": value
    }

    if meta:
        data["meta"] = meta

    return data

def run():
    timestamp = datetime.now().isoformat()
    send_datas = []

    # 🔹 CPU
    for name, value in get_cpu_temps():
        log_data(
            {
                "timestamp": timestamp,
                "name": name,
                "temperature": value
            },
            "cpu_temperature"
        )

        send_datas.append(
            build_send_data("CPU", name, value)
        )

    # 🔹 DISK
    for path, value in get_all_disk_temps().items():
        real_name = path.split("/")[-1]  # mais simples

        log_data(
            {
                "timestamp": timestamp,
                "name": real_name,
                "temperature": value,
                "device": path
            },
            "disk_temperature"
        )

        if value is not None:
            send_datas.append(
                build_send_data("DISK", real_name, value, meta=path)
            )

    if send_datas:
        send_to_api(send_datas)
