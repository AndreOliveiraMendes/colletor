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

def collect_snapshot():
    timestamp = datetime.now().isoformat()

    return {
        "timestamp": timestamp,
        "cpu": get_cpu_temps_hwmon(),
        "disk": get_all_disk_temps(),
        "battery": get_power(),
        "nodes": check_all_network_node()
    }

def run():
    snapshot = collect_snapshot()
    
    log_data(snapshot, "snapshot")
    send_to_api(snapshot)
    
    