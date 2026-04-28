import json
from datetime import datetime

from app.collector.battery import get_battery
from app.collector.cpu import get_cpu_temps, get_cpu_temps_hwmon
from app.collector.disk import get_all_disk_temps
from app.collector.tailscale import get_nodes
from app.utils import get_all_sys, get_sys_structure, print_structure


def debug():
    print("=== CPU ===")
    print("=== sensors ===")
    print(get_cpu_temps())

    print("=== hwmon ===")
    print(get_cpu_temps_hwmon())

    print("\n=== DISK ===")
    print(get_all_disk_temps())

    print("\n=== BATERY ===")
    print(get_battery())
    
    print("\n=== tailscale ===")
    print(get_nodes())
    
def explore():
    sys_dirs = get_all_sys()
    print("=== SYS ===")
    print(", ".join(sys_dirs))
    dir = input("choose one to explore:")
    if dir in sys_dirs:
        try:
            depth = int(input("max depth?"))
        except (ValueError, TypeError):
            depth = 2
        structure = get_sys_structure(dir, depth)
        print_structure(structure)
        y = input("save strucuter [y/n]:")
        if y == "y":
            date = datetime.now().isoformat()
            with open(f"sys_structure_{date}.json", "w") as f:
                json.dump(structure, f, indent=2)
    else:
        print("diretorio inexistente")

options = {
    "d":debug,
    "e":explore
}

def test():
    print("this is test mode")
    x = input("choose your option:\n[d: debug, e: explore]\n")

    if x in options:
        options[x]()
    else:
        print("invalid option")

