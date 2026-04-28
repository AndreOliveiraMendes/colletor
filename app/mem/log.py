import json
import os

from config import LOG_FOLDER


def log_data(data, filename):
    os.makedirs(LOG_FOLDER, mode=0o755, exist_ok=True)
    log_filepath = os.path.join(LOG_FOLDER, f"{filename}.jsonl")
    with open(log_filepath, "a", encoding='utf-8') as f:
        json.dump(data, f, default=str)
        f.write("\n")
