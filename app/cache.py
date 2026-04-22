import json
import os

from config import CACHE_FILE


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE) as f:
        return json.load(f)


def save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)