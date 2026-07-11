import json

import trackers.change_detector as change_detector


def test_first_run_detects_change(tmp_path, monkeypatch):

    snapshot_file = tmp_path / "snapshots.json"

    monkeypatch.setattr(
        change_detector,
        "SNAPSHOT_FILE",
        snapshot_file
    )

    result = change_detector.has_changed(
        "barclaycard",
        {"bonus_avios": 50000}
    )

    assert result is True

    saved = json.loads(snapshot_file.read_text())

    assert saved["barclaycard"]["bonus_avios"] == 50000


def test_identical_data_is_not_changed(tmp_path, monkeypatch):

    snapshot_file = tmp_path / "snapshots.json"

    monkeypatch.setattr(
        change_detector,
        "SNAPSHOT_FILE",
        snapshot_file
    )

    current = {
        "bonus_avios": 50000
    }

    change_detector.has_changed(
        "barclaycard",
        current
    )

    result = change_detector.has_changed(
        "barclaycard",
        current
    )

    assert result is False


def test_updated_data_detects_change(tmp_path, monkeypatch):

    snapshot_file = tmp_path / "snapshots.json"

    monkeypatch.setattr(
        change_detector,
        "SNAPSHOT_FILE",
        snapshot_file
    )

    change_detector.has_changed(
        "barclaycard",
        {"bonus_avios": 30000}
    )

    result = change_detector.has_changed(
        "barclaycard",
        {"bonus_avios": 50000}
    )

    assert result is True