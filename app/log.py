import json
import os

from config import LOG_FOLDER


def log_data(data, filename):
    if not LOG_FOLDER or not filename:
        return
    if not os.path.isdir(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    LOG_FILE = os.path.join(LOG_FOLDER, filename)
    with open(LOG_FILE, "a", encoding='utf-8') as f:
        f.write(json.dumps(data) + "\n")