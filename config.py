import os
import socket

from dotenv import load_dotenv

load_dotenv()

BASE_SYS = os.getenv("BASE_SYS", "/sys/class/")
HWMON_PATH = os.path.join(BASE_SYS, 'power_supply')
POWER_PATH = os.path.join(BASE_SYS, 'hwmon')
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

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")