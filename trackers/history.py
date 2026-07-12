"""
Store historical radar observations.

This module records every radar run using JSON Lines (JSONL) files.

Each execution appends the latest extracted data with a timestamp,
regardless of whether the data has changed.

This allows historical trends to be analysed separately from the
snapshot comparison process.

Each record includes:
    - Timestamp of the observation
    - Extracted article data
"""

import json
from pathlib import Path
from datetime import datetime, UTC


HISTORY_DIR = Path("storage/history")


def append_history(
    monitor_id: str,
    data: dict,
) -> None:
    """
    Append a radar observation to a history file.

    Records are stored in JSON Lines format, where each line contains
    one independent JSON object. This allows historical data to grow
    over time without needing to load the entire file into memory.

    Args:
        monitor_id:
            Name of the history file to append to.

        data:
            Dictionary containing extracted radar information.

    Example:
        append_history(
            "barclaycard",
            {
                "bonus_avios": 25000,
                "spend_requirement_gbp": 3000
            }
        )

        Creates:
            storage/history/barclaycard.jsonl
    """

    HISTORY_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    path = HISTORY_DIR / f"{monitor_id}.jsonl"

    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        **data
    }

    with open(path, "a", encoding="utf-8") as f:
        f.write(
            json.dumps(record)
            + "\n"
        )