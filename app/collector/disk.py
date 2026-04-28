import subprocess

from app.mem.cache import load_cache, save_cache

CACHE = load_cache()

def detect_device_type(disk):
    types = ["auto", "sat", "sat,12", "sat,16", "scsi"]

    for t in types:
        cmd = ["sudo", "smartctl", "-A", "-d", t, disk, "-T", "permissive"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stdout:
            temp = extract_temperature(result.stdout)
            if temp is not None:
                return t

    return None

def get_real_disks():
    result = subprocess.run(
        ["lsblk", "-dn", "-o", "NAME,TYPE,SIZE"],
        capture_output=True,
        text=True
    )

    disks = []
    for line in result.stdout.splitlines():
        name, dtype, size = line.split()

        if dtype == "disk" and size != "0B":
            disks.append(f"/dev/{name}")

    return disks

def extract_temperature(output):
    for line in output.splitlines():
        if "Temperature_Celsius" in line:
            try:
                return int(line.split()[-1])
            except:
                pass

        elif "Airflow_Temperature_Cel" in line:
            try:
                return int(line.split()[9])  # fallback
            except:
                pass

    return None

def get_disk_temp(disk):
    global CACHE

    dtype = CACHE.get(disk, "unknown")

    # nunca testado ainda
    if dtype == "unknown":
        dtype = detect_device_type(disk)
        CACHE[disk] = dtype
        save_cache(CACHE)

    # não suporta → nem tenta mais
    if dtype is None:
        return None

    cmd = ["sudo", "smartctl", "-A", "-d", dtype, disk]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        return extract_temperature(result.stdout)

    return None

def get_all_disk_temps():
    disks = get_real_disks()
    temps = {}

    for d in disks:
        temp = get_disk_temp(d)
        temps[d] = temp if temp is not None else None

    return temps

def get_disk():
    out = []

    for path, value in get_all_disk_temps().items():
        out.append({
            "type": "temperature",
            "device": "DISK",
            "source": "local",
            "name": path.split("/")[-1],
            "value": value,
            "meta": {"path": path}
        })

    return out