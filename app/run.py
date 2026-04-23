from datetime import datetime

from app.battery import get_power
from app.cpu import get_cpu_temps_hwmon
from app.disk import get_all_disk_temps
from app.log import log_data
from app.sender import send_to_api
from app.tailscale import check_all_network_node
from config import HOSTIP, HOSTNAME


def build_send_data(info_type, info_source, target, device_type, name, value, value_text = None, meta=None):
    data = {
        "type": info_type,
        "source": info_source,
        "host_name": HOSTNAME,
        "host_ip": HOSTIP,
        "target": target,
        "device_type": device_type,
        "name": name,
        "value": value
    }
    
    if value_text:
        data["value_text"] = value_text

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
            build_send_data("temperature", "local", None, "CPU", name, value)
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
                build_send_data("temperature", "local", None, "DISK", real_name, value, meta=path)
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
            build_send_data("battery", "local", None, None, None, value, meta=data)
        )
        
    nodes = check_all_network_node()
    
    for raw in nodes:
        log_data(
            {
                "timestamp": timestamp,
                "node": raw.get('name'),
                "tailscale": raw.get('tailscale'),
                "local": raw.get('local')
            },
            "node"
        )
        
        send_datas.append(
            build_send_data(
                "network",
                "remote",
                raw.get('name'),
                'tailscale',
                raw.get('name'),
                raw.get('ip'),
                raw.get('tailscale'),
                meta={
                    "tailscale": raw.get('tailscale'),
                    "local": raw.get('local')
                }
            )
        ) 

    if send_datas:
        send_to_api(send_datas)

