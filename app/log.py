import json
import os

from config import LOG_FOLDER


def log_data(data, filename):
    if not LOG_FOLDER or not filename:
        return
    os.makedirs("logs", exist_ok=True)
    log_filepath = os.path.join(LOG_FOLDER, f"{filename}.jsonl")
    with open(log_filepath, "a", encoding='utf-8') as f:
        json.dump(data, f)
        f.write("\n")