import hashlib
import pickle
from pathlib import Path

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)


def cache_path(key: str) -> Path:
    filename = hashlib.md5(key.encode()).hexdigest() + ".pkl"
    return CACHE_DIR / filename


def load_cache(key: str):

    path = cache_path(key)

    if path.exists():
        with open(path, "rb") as f:
            return pickle.load(f)

    return None


def save_cache(key: str, data):

    path = cache_path(key)

    with open(path, "wb") as f:
        pickle.dump(data, f)