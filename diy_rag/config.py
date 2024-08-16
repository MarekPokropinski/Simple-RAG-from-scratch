import json
from pathlib import Path


def load_config():
    with open(Path(__file__).parent.parent / "config.json", "r") as f:
        config = json.load(f)
        return config
