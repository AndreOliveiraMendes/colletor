import subprocess


def check_node(node):
    for _ in range(3):
        result = subprocess.run(
            ["tailscale", "ping", "-c", "1", node],
            capture_output=True,
            text=True
        )

        if "pong" in result.stdout:
            return True

    return False