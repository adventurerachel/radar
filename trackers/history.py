import json
from pathlib import Path
from datetime import datetime, UTC


HISTORY_DIR = Path("storage/history")


def append_history(history_file, data):

    HISTORY_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = history_file + ".jsonl"

    path = HISTORY_DIR / f"{history_file}.jsonl"

    record = {
        "timestamp": datetime.now(UTC).isoformat(),
        **data
    }

    with open(path, "a", encoding="utf-8") as f:
        f.write(
            json.dumps(record)
            + "\n"
        )