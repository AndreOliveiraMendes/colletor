import subprocess


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
    commands = [
        ["sudo", "smartctl", "-A", disk],              # direto
        ["sudo", "smartctl", "-A", "-d", "sat", disk], # USB
        ["sudo", "smartctl", "-A", "-d", "scsi", disk]
    ]

    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.stdout:
            temp = extract_temperature(result.stdout)
            if temp is not None:
                return temp

    return None


def get_all_disk_temps():
    disks = get_real_disks()
    temps = {}

    for d in disks:
        temp = get_disk_temp(d)
        temps[d] = temp if temp is not None else None

    return temps
