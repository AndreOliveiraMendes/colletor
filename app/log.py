import json

from config import LOG


def log_data(data):
    if not LOG:
        return
    with open(LOG, "a", encoding='utf-8') as f:
        f.write(json.dumps(data) + "\n")