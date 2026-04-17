import json
import subprocess


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