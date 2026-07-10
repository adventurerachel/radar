import json
from pathlib import Path


SNAPSHOT_FILE = Path("storage/snapshots.json")


def load_snapshots():

    if not SNAPSHOT_FILE.exists():
        return {}

    with open(SNAPSHOT_FILE, "r") as f:
        return json.load(f)


def save_snapshots(data):

    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(
            data,
            f,
            indent=2
        )


def has_changed(name, current):

    snapshots = load_snapshots()

    previous = snapshots.get(name)

    # First ever run
    if previous is None:

        snapshots[name] = current
        save_snapshots(snapshots)

        return True

    # No change
    if previous == current:
        return False

    # Change detected
    snapshots[name] = current
    save_snapshots(snapshots)

    return True