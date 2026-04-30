from datetime import datetime

import yaml

from app.collector.battery import get_battery
from app.collector.cpu import get_cpu
from app.collector.disk import get_disk
from app.collector.tailscale import get_nodes
from app.runner.run import log_datas, process_and_send

COLLECTORS = {
    "cpu": get_cpu,
    "disk": get_disk,
    "battery": get_battery,
    "nodes": get_nodes,
}

PROCESSORS = {
    "log": log_datas,
    "send": process_and_send,
}

def load_config(path="data/runs.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def resolve_run(name, config):
    run = config["runs"][name]

    collectors = list(run.get("collectors", []))
    processors = list(run.get("processors", []))

    for included in run.get("include", []):
        sub = resolve_run(included, config)
        collectors += sub["collectors"]
        processors += sub["processors"]

    return {
        "collectors": collectors,
        "processors": processors
    }

def run_from_config(run_name, config):
    now = datetime.now()
    resolved = resolve_run(run_name, config)

    snapshot = {
        "timestamp": now.isoformat(),
        "metrics": []
    }

    for name in resolved["collectors"]:
        try:
            fn = COLLECTORS[name]
        except KeyError:
            raise ValueError(f"Collector desconhecido: {name}")

        snapshot["metrics"].extend(fn())

    for name in resolved["processors"]:
        try:
            fn = PROCESSORS[name]
        except KeyError:
            raise ValueError(f"Processor desconhecido: {name}")

        fn(snapshot)
