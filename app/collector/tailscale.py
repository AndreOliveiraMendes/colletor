import json
import subprocess


def get_self_ips():
    result = subprocess.run(
        ["tailscale", "status", "--json"],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    return set(data["Self"]["TailscaleIPs"])


def list_nodes_raw():
    result = subprocess.run(
        ["tailscale", "status"],
        capture_output=True,
        text=True
    )

    nodes = []

    for line in result.stdout.splitlines():
        if not line.strip():
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        nodes.append({
            "ip": parts[0],
            "name": parts[1],
        })

    return nodes

def check_node(node_ip, self_ips):
    # self
    if node_ip in self_ips:
        status = subprocess.run(
            ["tailscale", "status"],
            capture_output=True
        )
        return "self (online)" if status.returncode == 0 else "self (error)"

    # outros
    for _ in range(3):
        result = subprocess.run(
            ["tailscale", "ping", "-c", "1", node_ip],
            capture_output=True,
            text=True
        )

        out = result.stdout.lower()

        if "pong" in out:
            return "relay" if "via derp" in out else "direct"

    return "offline"

def get_nodes():
    nodes = list_nodes_raw()
    self_ips = get_self_ips()

    metrics = []

    for n in nodes:
        ts_status = check_node(n["ip"], self_ips)

        metrics.append({
            "type": "network",
            "device": "tailscale",
            "source": "remote",
            "target": n["name"],
            "name": n["name"],
            "value": n["ip"],
            "meta": {
                "tailscale": ts_status,
                "local": n["ip"] in self_ips
            }
        })

    return metrics