import json
import os
import subprocess

from config import POWER_PATH


def get_cpu_temps():
    result = subprocess.run(
        ["sensors", "-j"],
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)
    temps = []

    for chip in data.values():
        for key, value in chip.items():
            if "Core" in key:
                for k, v in value.items():
                    if k.endswith("_input"):
                        temps.append((key, int(v)))

    return temps

def get_cpu_temps_hwmon():
    for hw in os.listdir(POWER_PATH):
        path = os.path.join(POWER_PATH, hw)

        try:
            with open(os.path.join(path, "name")) as f:
                if f.read().strip() != "coretemp":
                    continue
        except:
            continue

        temps = []

        for file in os.listdir(path):
            if file.startswith("temp") and file.endswith("_input"):
                idx = file.replace("temp", "").replace("_input", "")
                label_file = f"temp{idx}_label"

                label = f"Core {idx}"

                label_path = os.path.join(path, label_file)
                if os.path.exists(label_path):
                    with open(label_path) as f:
                        label = f.read().strip()

                with open(os.path.join(path, file)) as f:
                    temp = int(f.read()) / 1000

                temps.append((label, temp))

        return temps

    return []

def get_cpu():
    return [
        {
            "type": "temperature",
            "device": "CPU",
            "source": "local",
            "name": name,
            "value": value
        }
        for name, value in get_cpu_temps_hwmon()
    ]