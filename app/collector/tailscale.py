import subprocess
import json
import re

def tailscale_status_json():
    result = subprocess.run(
        ["tailscale", "status", "--json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)


def ping_node(ip):
    result = subprocess.run(
        ["tailscale", "ping", "-c", "1", ip],
        capture_output=True,
        text=True
    )

    out = result.stdout.lower()

    status = "offline"
    latency = None

    if "pong" in out:
        status = "relay" if "via derp" in out else "direct"

        # tenta extrair latência (ex: time=12ms)
        match = re.search(r'time[=<]\s*([\d\.]+)\s*ms', out)
        if match:
            latency = float(match.group(1))

    return status, latency


def get_nodes(mode="simplified"):
    data = tailscale_status_json()

    self_ips = set(data["Self"]["TailscaleIPs"])
    all_nodes = [data["Self"]] + list(data.get("Peer", {}).values())

    metrics = []

    for node in all_nodes:
        ips = node.get("TailscaleIPs", [])
        ip = ips[0] if ips else None
        name = node.get("HostName") or node.get("DNSName")

        is_self = ip in self_ips
        online = node.get("Online", False)

        ts_status = None
        latency = None

        # 🔹 modo simplified
        if mode == "simplified":
            ts_status = "online" if online else "offline"

        # 🔹 modo normal
        elif mode == "normal":
            if is_self:
                ts_status = "self"
            elif online:
                ts_status, _ = ping_node(ip)
            else:
                ts_status = "offline"

        # 🔹 modo detailed
        elif mode == "detailed":
            if is_self:
                ts_status = "self"
            elif online:
                ts_status, latency = ping_node(ip)
            else:
                ts_status = "offline"

        metrics.append({
            "type": "network",
            "device": "tailscale",
            "source": "remote",
            "target": name,
            "name": name,
            "value": ip,
            "meta": {
                "tailscale": ts_status,
                "online": online,
                "self": is_self,
                **({"latencia": latency} if mode == "detailed" and latency is not None else {})
            }
        })

    return metrics