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

def check_node(node):
    self_ips = get_self_ips()

    if node in self_ips:
        return "direct (host)"

    for _ in range(3):
        result = subprocess.run(
            ["tailscale", "ping", "-c", "1", node],
            capture_output=True,
            text=True
        )

        out = result.stdout.lower()

        if "pong" in out:
            if "via derp" in out:
                return "relay"
            return "direct"

    return "offline"

def get_nodes():
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

        ip = parts[0]
        name = parts[1]
        status = "online" if "offline" not in line else "offline"

        nodes.append({
            "ip": ip,
            "name": name,
            "status": status
        })

    return nodes

def check_all_network_node():
    nodes = get_nodes()
    result = []

    for n in nodes:
        ts_status = check_node(n["ip"])

        # exemplo simples de ping local
        local = subprocess.run(
            ["ping", "-c", "1", n["ip"]],
            capture_output=True
        )

        local_status = "up" if local.returncode == 0 else "down"

        result.append({
            "name": n["name"],
            "ip": n["ip"],
            "tailscale": ts_status,
            "local": local_status
        })

    return result