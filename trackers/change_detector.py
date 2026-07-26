"""
Detect changes in monitored article data.

This module maintains a local snapshot of previously observed values
and compares them against newly extracted data.

The snapshot file acts as persistent memory between radar runs:

    First run:
        No previous data exists → store snapshot → report change

    Later runs:
        Same data → no alert
        Different data → update snapshot → report change
"""

import json
from pathlib import Path
from datetime import datetime, UTC


SNAPSHOT_FILE = Path("storage/snapshots.json")


def load_snapshots() -> dict:
    """
    Load previously stored snapshots.

    Returns:
        Dictionary containing previously recorded values.
        Returns an empty dictionary if no snapshot file exists.
    """

    if not SNAPSHOT_FILE.exists():
        return {}

    with open(SNAPSHOT_FILE, "r") as f:
        return json.load(f)


def save_snapshots(data: dict) -> None:
    """
    Save current snapshots to disk.

    Args:
        data:
            Dictionary containing the latest monitored values.
    """

    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(
            data,
            f,
            indent=2
        )


def has_changed(monitor_id: str, current: dict) -> bool:
    """
    Determine whether monitored data has changed since the last run.

    If this is the first time a source is checked, the current value
    is stored and treated as a change.

    If the current value differs from the stored snapshot, the snapshot
    is updated and a change is reported.

    Args:
        monitor_id:
            Identifier for the monitored source.

        current:
            Newly extracted data from the source.

    Returns:
        True if the data is new or has changed.
        False if the data matches the stored snapshot.
    """

    snapshots = load_snapshots()

    previous = snapshots.get(monitor_id)
def has_changed(
    monitor_id: str,
    current: dict,
) -> bool:
    """
    Determine whether monitored data has changed since the last run.
    """

    snapshots = load_snapshots()

    previous = snapshots.get(
        monitor_id
    )

    current_snapshot = {
        **current,
        "last_checked": datetime.now(
            UTC
        ).isoformat(),
    }

    # First ever run
    if previous is None:

        snapshots[monitor_id] = (
            current_snapshot
        )

        save_snapshots(
            snapshots
        )

        return True

    # Compare without metadata
    previous_comparable = {
        k: v
        for k, v in previous.items()
        if k != "last_checked"
    }

    if previous_comparable == current:

        # Update timestamp even when
        # monitored data is unchanged
        snapshots[monitor_id] = (
            current_snapshot
        )

        save_snapshots(
            snapshots
        )

        return False

    # Change detected
    snapshots[monitor_id] = (
        current_snapshot
    )

    save_snapshots(
        snapshots
    )

    return True
   