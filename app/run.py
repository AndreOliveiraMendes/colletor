from datetime import datetime

from app.battery import get_power
from app.cpu import get_cpu_temps_hwmon
from app.disk import get_all_disk_temps
from app.log import log_data
from app.sender import send_to_api
from config import HOSTIP, HOSTNAME


def build_send_data(info_type, info_source, device_type, name, value, meta=None):
    data = {
        "type": info_type,
        "source": info_source,
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
    for name, value in get_cpu_temps_hwmon():
        log_data(
            {
                "timestamp": timestamp,
                "name": name,
                "temperature": value
            },
            "cpu_temperature"
        )

        send_datas.append(
            build_send_data("temperature", "local", "CPU", name, value)
        )

    # 🔹 DISK
    for path, value in get_all_disk_temps().items():
        real_name = path.split("/")[-1]  # mais simples

        path_file = "disk_temperature" if value else "disk_temperature_strange"
        log_data(
            {
                "timestamp": timestamp,
                "name": real_name,
                "temperature": value,
                "device": path
            },
            path_file
        )

        if value is not None:
            send_datas.append(
                build_send_data("temperature", "local", "DISK", real_name, value, meta=path)
            )
            
    # 🔹 BATTERY (todo: add suport for multiple batteries)
    data = get_power()
    
    timestamp = data.get("timestamp")
    ac_connected = data.get("ac_online")
    status = data.get("status")
    value = data.get("capacity")
    
    log_data(
        {
            "timestamp": timestamp,
            "ac_connected": ac_connected,
            "status": status,
            "value": value
        },
        "battery"
    )
    
    if value:
        send_datas.append(
            build_send_data("battery", "local", None, None, value, data)
        )

    if send_datas:
        send_to_api(send_datas)

"""
    type TEXT NOT NULL,
    source TEXT NOT NULL,
    host_name TEXT NOT NULL,
    host_ip TEXT NOT NULL,
    target TEXT,
    device_type TEXT,
    name TEXT,
    value REAL,
    value_text TEXT,
    meta TEXT
"""
