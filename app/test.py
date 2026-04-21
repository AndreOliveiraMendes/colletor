import json
from datetime import datetime

from app.battery import get_power
from app.cpu import get_cpu_temps, get_cpu_temps_hwmon
from app.disk import get_all_disk_temps
from app.tailscale import check_all
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
    print(get_power())
    
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
        
def new():
    print("=== testing new functions ===")
    out = check_all()
    
    for raw in out:
        data = [f"{key}:{value}" for key, value in raw.items()]
        print(", ".join(data))

options = {
    "d":debug,
    "e":explore,
    "n":new
}

def test():
    print("this is test mode")
    x = input("choose your option:\n[d: debug, e: explore, n: new functions]\n")

    if x in options:
        options[x]()
    else:
        print("invalid option")

