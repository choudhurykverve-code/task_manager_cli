import json
import os
import tempfile

import pytest

from models.enum import Priority, Status
from models.task import Task
from storage.json_storage import JsonStorage


@pytest.fixture
def tmp_json(tmp_path):
    """Return a path to a temporary JSON file inside a temp directory."""
    return str(tmp_path / "tasks.json")


# ---------------------------------------------------------------------------
# save_tasks / load_tasks round-trip
# ---------------------------------------------------------------------------

class TestSaveAndLoad:

    def test_save_and_load_round_trip(self, tmp_json):
        storage = JsonStorage(tmp_json)
        task = Task("save me", description="d", priority=Priority.HIGH)
        storage.save_tasks([task])

        loaded = storage.load_tasks()
        assert len(loaded) == 1
        assert loaded[0].id == task.id
        assert loaded[0].title == "save me"
        assert loaded[0].priority == Priority.HIGH

    def test_save_empty_list(self, tmp_json):
        storage = JsonStorage(tmp_json)
        storage.save_tasks([])

        loaded = storage.load_tasks()
        assert loaded == []

    def test_save_multiple_tasks(self, tmp_json):
        storage = JsonStorage(tmp_json)
        tasks = [
            Task("a", priority=Priority.LOW),
            Task("b", priority=Priority.MEDIUM),
            Task("c", priority=Priority.HIGH),
        ]
        storage.save_tasks(tasks)

        loaded = storage.load_tasks()
        assert len(loaded) == 3
        titles = {t.title for t in loaded}
        assert titles == {"a", "b", "c"}

    def test_overwrite_on_save(self, tmp_json):
        storage = JsonStorage(tmp_json)
        storage.save_tasks([Task("first")])
        storage.save_tasks([Task("second")])

        loaded = storage.load_tasks()
        assert len(loaded) == 1
        assert loaded[0].title == "second"


# ---------------------------------------------------------------------------
# load_tasks edge cases
# ---------------------------------------------------------------------------

class TestLoadEdgeCases:

    def test_load_missing_file_returns_empty(self, tmp_path):
        storage = JsonStorage(str(tmp_path / "does_not_exist.json"))
        assert storage.load_tasks() == []

    def test_load_corrupt_json_returns_empty(self, tmp_json):
        with open(tmp_json, "w") as f:
            f.write("NOT VALID JSON {{{")

        storage = JsonStorage(tmp_json)
        assert storage.load_tasks() == []

    def test_load_preserves_completed_status(self, tmp_json):
        storage = JsonStorage(tmp_json)
        task = Task("done")
        task.mark_completed()
        storage.save_tasks([task])

        loaded = storage.load_tasks()
        assert loaded[0].is_completed is True
        assert loaded[0].completed_at is not None


# ---------------------------------------------------------------------------
# File content validation
# ---------------------------------------------------------------------------

class TestFileContent:

    def test_file_contains_valid_json(self, tmp_json):
        storage = JsonStorage(tmp_json)
        storage.save_tasks([Task("j")])

        with open(tmp_json) as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["title"] == "j"
