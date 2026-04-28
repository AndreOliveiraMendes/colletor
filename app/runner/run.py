from datetime import datetime

from app.channel.sender import send_to_api
from app.collector.battery import get_power
from app.collector.cpu import get_cpu_temps_hwmon
from app.collector.disk import get_all_disk_temps
from app.collector.tailscale import check_all_network_node
from app.mem.log import log_data
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
        "value": value,
        "metric": f"{info_type}.{device_type}"
    }
    
    if value_text:
        data["value_text"] = value_text

    if meta:
        data["meta"] = meta

    return data

def run():
    # setup
    timestamp = datetime.now().isoformat()
    send_datas = []
    
    # collect data
    
    temps_cpu = get_cpu_temps_hwmon()
    temps_disk = get_all_disk_temps()
    battery = get_power()
    nodes = check_all_network_node()
    
    # log and send
    
    # 🔹 CPU
    for name, value in temps_cpu:
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
    for path, value in temps_disk.items():
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
    
    ac_connected = battery.get("ac_online")
    status = battery.get("status")
    value = battery.get("capacity")
    
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
            build_send_data("battery", "local", None, "battery", None, value, meta=battery)
        )
<<<<<<< HEAD

    # 🔹 BATTERY (todo: add suport for multiple batteries)
    nodes = check_all_network_node()
=======
>>>>>>> 10f9e72 (feat: refactor data collection in run function and enhance build_send_data structure)
    
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
                    "local": False
                }
            )
        ) 

    if send_datas:
        send_to_api(send_datas)

