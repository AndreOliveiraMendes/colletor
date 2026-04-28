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

def collect_snapshot_1():
    timestamp = datetime.now().isoformat()

    return {
        "timestamp": timestamp,
        "cpu": get_cpu_temps_hwmon(),
        "disk": get_all_disk_temps(),
        "battery": get_power()
    }

def collect_snapshot_2():
    timestamp = datetime.now().isoformat()

    return {
        "timestamp": timestamp,
        "nodes": check_all_network_node()
    }
    
def log_datas(snapshot):
    if 'cpu' in snapshot:
        for name, value in snapshot.get('cpu'):
            log_data(
                {
                    "timestamp": snapshot.get('timestamp'),
                    "name": name,
                    "temperature": value
                },
                "cpu_temperature"
            )
        
    if 'disk' in snapshot:
        for path, value in snapshot.get('disk').items():
            real_name = path.split("/")[-1]  # mais simples

            path_file = "disk_temperature" if value else "disk_temperature_strange"
            log_data(
                {
                    "timestamp": snapshot.get('timestamp'),
                    "name": real_name,
                    "temperature": value,
                    "device": path
                },
                path_file
            )
    
    if 'battery' in snapshot:
        battery = snapshot.get('battery')
        ac_connected = battery.get("ac_online")
        status = battery.get("status")
        value = battery.get("capacity")
    
        log_data(
            {
                "timestamp": snapshot.get('timestamp'),
                "ac_connected": ac_connected,
                "status": status,
                "value": value
            },
            "battery"
        )
    
    if 'nodes' in snapshot:
        for raw in snapshot.get('nodes'):
            log_data(
                {
                    "timestamp": snapshot.get('timestamp'),
                    "node": raw.get('name'),
                    "tailscale": raw.get('tailscale'),
                    "local": raw.get('local')
                },
                "node"
            )
        
def process_and_send(snapshot):
    send_datas = []
    
    if 'cpu' in snapshot:
        for name, value in snapshot.get('cpu'):
            send_datas.append(
                build_send_data("temperature", "local", None, "CPU", name, value)
            )

    if 'disk' in snapshot:
        for path, value in snapshot.get('disk').items():
            real_name = path.split("/")[-1]  # mais simples

            if value is not None:
                send_datas.append(
                    build_send_data("temperature", "local", None, "DISK", real_name, value, meta=path)
                )
    
    if 'battery' in snapshot:
        battery = snapshot.get('battery')
        ac_connected = battery.get("ac_online")
        status = battery.get("status")
        value = battery.get("capacity")
    
        if value:
            send_datas.append(
                build_send_data("battery", "local", None, "battery", None, value, meta=battery)
            )

    if 'nodes' in snapshot:
        for raw in snapshot.get('nodes'):
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

def run1():
    snapshot = collect_snapshot_1()
    
    log_datas(snapshot)
    process_and_send(snapshot)

def run2():
    snapshot = collect_snapshot_2()

    log_datas(snapshot)
    process_and_send(snapshot)
