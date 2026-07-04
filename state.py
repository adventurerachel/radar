import json
from pathlib import Path


STATE_DIR = Path("data/state")
STATE_DIR.mkdir(parents=True, exist_ok=True)


def load_state(name: str) -> dict:
    path = STATE_DIR / f"{name}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_state(name: str, state: dict):
    path = STATE_DIR / f"{name}.json"
    path.write_text(json.dumps(state, indent=2))