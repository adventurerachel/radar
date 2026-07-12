"""
Tests for radar change detection.

These tests verify that the change detector correctly compares newly
extracted data against previously stored snapshots.

The tests use temporary snapshot files rather than the real storage
location, ensuring they:
    - Do not modify real radar state
    - Run independently
    - Can be executed repeatedly with predictable results

Covered behaviours:
    - First run is treated as a detected change
    - Identical data does not trigger a change
    - Updated data triggers a change
"""

import json

import trackers.change_detector as change_detector


def test_first_run_detects_change(tmp_path, monkeypatch):
    """
    Treat the first observation of a monitor as a change and save
    the initial snapshot.
    """

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
    """
    Return False when the current data matches the stored snapshot.
    """

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
    """
    Return True when monitored data differs from the stored snapshot.
    """

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

def test_changed_data_updates_snapshot(tmp_path, monkeypatch):
    """
    When a change is detected, save the new data as the latest snapshot.
    """

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

    saved = json.loads(snapshot_file.read_text())

    assert saved["barclaycard"]["bonus_avios"] == 50000