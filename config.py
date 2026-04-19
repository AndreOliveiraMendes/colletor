import os
import socket

from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("BASE", "/sys/class/power_supply")
SERVER = os.getenv("SERVER", "server")
LOG_FOLDER = os.getenv("LOG_FOLDER", "/var/log")


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


HOSTNAME = os.getenv("HOSTNAME", socket.gethostname())
HOSTIP = os.getenv("HOSTIP") or get_host_ip()