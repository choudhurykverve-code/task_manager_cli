import uuid
from datetime import datetime, timezone

import pytest

from models.enum import Priority, Status
from models.task import Task


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------

class TestTaskCreation:

    def test_default_values(self):
        task = Task("Buy milk")
        assert task.title == "Buy milk"
        assert task.description is None
        assert task.priority == Priority.MEDIUM
        assert task.status == Status.PENDING
        assert task.is_completed is False
        assert task.completed_at is None
        # id should be a valid UUID string
        uuid.UUID(task.id)

    def test_custom_priority_and_description(self):
        task = Task("Deploy", description="Ship v2", priority=Priority.HIGH)
        assert task.title == "Deploy"
        assert task.description == "Ship v2"
        assert task.priority == Priority.HIGH

    def test_title_is_stripped(self):
        task = Task("  padded title  ")
        assert task.title == "padded title"

    def test_empty_title_raises(self):
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task("")

    def test_whitespace_only_title_raises(self):
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task("   ")

    def test_invalid_priority_raises(self):
        with pytest.raises(ValueError, match="Priority must be a Priority enum"):
            Task("task", priority="high")

    def test_created_at_is_utc(self):
        before = datetime.now(timezone.utc)
        task = Task("t")
        after = datetime.now(timezone.utc)
        assert before <= task.created_at <= after


# ---------------------------------------------------------------------------
# mark_completed
# ---------------------------------------------------------------------------

class TestMarkCompleted:

    def test_mark_completed(self):
        task = Task("t")
        task.mark_completed()
        assert task.status == Status.COMPLETED
        assert task.is_completed is True
        assert task.completed_at is not None

    def test_mark_completed_twice_raises(self):
        task = Task("t")
        task.mark_completed()
        with pytest.raises(ValueError, match="already completed"):
            task.mark_completed()


# ---------------------------------------------------------------------------
# Update helpers
# ---------------------------------------------------------------------------

class TestUpdateMethods:

    def test_update_title(self):
        task = Task("old")
        old_updated = task._updated_at
        task.update_title("new")
        assert task.title == "new"
        assert task._updated_at >= old_updated

    def test_update_title_empty_raises(self):
        task = Task("t")
        with pytest.raises(ValueError, match="Title cannot be empty"):
            task.update_title("")

    def test_update_description(self):
        task = Task("t")
        task.update_description("desc")
        assert task.description == "desc"

    def test_update_description_to_none(self):
        task = Task("t", description="old")
        task.update_description(None)
        assert task.description is None

    def test_update_priority(self):
        task = Task("t", priority=Priority.LOW)
        task.update_priority(Priority.HIGH)
        assert task.priority == Priority.HIGH

    def test_update_priority_invalid_raises(self):
        task = Task("t")
        with pytest.raises(ValueError, match="Priority can be only enum"):
            task.update_priority("low")


# ---------------------------------------------------------------------------
# Serialization round-trip
# ---------------------------------------------------------------------------

class TestSerialization:

    def test_to_dict_fields(self):
        task = Task("t", description="d", priority=Priority.HIGH)
        d = task.to_dict()
        assert d["title"] == "t"
        assert d["description"] == "d"
        assert d["priority"] == "HIGH"
        assert d["status"] == "PENDING"
        assert d["completed_at"] is None
        # id is a valid UUID string
        uuid.UUID(d["id"])
        # timestamps are ISO-format strings
        datetime.fromisoformat(d["created_at"])
        datetime.fromisoformat(d["updated_at"])

    def test_round_trip(self):
        original = Task("roundtrip", description="d", priority=Priority.LOW)
        restored = Task.from_dict(original.to_dict())
        assert restored.id == original.id
        assert restored.title == original.title
        assert restored.description == original.description
        assert restored.priority == original.priority
        assert restored.status == original.status

    def test_round_trip_completed_task(self):
        original = Task("done")
        original.mark_completed()
        restored = Task.from_dict(original.to_dict())
        assert restored.is_completed is True
        assert restored.completed_at is not None
