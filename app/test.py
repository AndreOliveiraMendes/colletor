from app.battery import get_power
from app.cpu import get_cpu_temps, get_cpu_temps_hwmon
from app.disk import get_all_disk_temps

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

options = {
    "d":debug
}

def test():
    print("this is test mode")
    x = input("choose your option:\n[d: debug]\n")

    if x in options:
        options[x]()
    else:
        print("invalid option")

