from app.channel.sender import send_to_api
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

def log_datas(snapshot):
    ts = snapshot["timestamp"]

    for m in snapshot["metrics"]:
        log_data(
            {
                "timestamp": ts,
                **m
            },
            f"{m['type']}_{m['device']}".lower()
        )
        
def process_and_send(snapshot):
    send_datas = []

    for m in snapshot["metrics"]:
        send_datas.append(
            build_send_data(
                m["type"],
                "local",  # ou vem do collector
                m.get("target"),
                m["device"],
                m.get("name"),
                m["value"],
                meta=m.get("meta")
            )
        )

    if send_datas:
        send_to_api(send_datas)