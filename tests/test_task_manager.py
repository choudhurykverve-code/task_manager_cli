import pytest

from models.enum import Priority, Status
from models.task import Task
from services.task_manager import TaskManager


class FakeStorage:
    """In-memory storage stub that avoids touching the filesystem."""

    def __init__(self, initial_tasks=None):
        self._tasks = list(initial_tasks or [])
        self.save_count = 0

    def load_tasks(self):
        return list(self._tasks)

    def save_tasks(self, tasks):
        self._tasks = list(tasks)
        self.save_count += 1


# ---------------------------------------------------------------------------
# add_task
# ---------------------------------------------------------------------------

class TestAddTask:

    def test_add_task_returns_task(self):
        manager = TaskManager(FakeStorage())
        task = manager.add_task("new task")
        assert task.title == "new task"
        assert task.priority == Priority.MEDIUM

    def test_add_task_with_options(self):
        manager = TaskManager(FakeStorage())
        task = manager.add_task("t", description="d", priority=Priority.HIGH)
        assert task.description == "d"
        assert task.priority == Priority.HIGH

    def test_add_task_persists(self):
        storage = FakeStorage()
        manager = TaskManager(storage)
        manager.add_task("t")
        assert storage.save_count == 1

    def test_add_task_increments_count(self):
        manager = TaskManager(FakeStorage())
        manager.add_task("a")
        manager.add_task("b")
        assert len(manager.get_all_tasks()) == 2


# ---------------------------------------------------------------------------
# get_task
# ---------------------------------------------------------------------------

class TestGetTask:

    def test_get_existing_task(self):
        manager = TaskManager(FakeStorage())
        created = manager.add_task("x")
        fetched = manager.get_task(created.id)
        assert fetched.id == created.id

    def test_get_missing_task_raises(self):
        manager = TaskManager(FakeStorage())
        with pytest.raises(KeyError, match="Task does not exist"):
            manager.get_task("nonexistent-id")


# ---------------------------------------------------------------------------
# delete_task
# ---------------------------------------------------------------------------

class TestDeleteTask:

    def test_delete_task(self):
        manager = TaskManager(FakeStorage())
        task = manager.add_task("t")
        manager.delete_task(task.id)
        assert len(manager.get_all_tasks()) == 0

    def test_delete_missing_task_raises(self):
        manager = TaskManager(FakeStorage())
        with pytest.raises(KeyError, match="Task does not exist"):
            manager.delete_task("bad-id")


# ---------------------------------------------------------------------------
# complete_task
# ---------------------------------------------------------------------------

class TestCompleteTask:

    def test_complete_task(self):
        manager = TaskManager(FakeStorage())
        task = manager.add_task("t")
        manager.complete_task(task.id)
        assert manager.get_task(task.id).is_completed is True

    def test_complete_already_completed_raises(self):
        manager = TaskManager(FakeStorage())
        task = manager.add_task("t")
        manager.complete_task(task.id)
        with pytest.raises(ValueError, match="already completed"):
            manager.complete_task(task.id)


# ---------------------------------------------------------------------------
# update_task
# ---------------------------------------------------------------------------

class TestUpdateTask:

    def test_update_title(self):
        manager = TaskManager(FakeStorage())
        task = manager.add_task("old")
        manager.update_task(task.id, title="new")
        assert manager.get_task(task.id).title == "new"

    def test_update_description(self):
        manager = TaskManager(FakeStorage())
        task = manager.add_task("t")
        manager.update_task(task.id, description="d")
        assert manager.get_task(task.id).description == "d"

    def test_update_priority(self):
        manager = TaskManager(FakeStorage())
        task = manager.add_task("t")
        manager.update_task(task.id, priority=Priority.LOW)
        assert manager.get_task(task.id).priority == Priority.LOW

    def test_update_missing_task_raises(self):
        manager = TaskManager(FakeStorage())
        with pytest.raises(KeyError):
            manager.update_task("missing", title="x")


# ---------------------------------------------------------------------------
# get_all_tasks
# ---------------------------------------------------------------------------

class TestGetAllTasks:

    def test_empty_manager(self):
        manager = TaskManager(FakeStorage())
        assert manager.get_all_tasks() == []

    def test_returns_all_added(self):
        manager = TaskManager(FakeStorage())
        manager.add_task("a")
        manager.add_task("b")
        manager.add_task("c")
        assert len(manager.get_all_tasks()) == 3


# ---------------------------------------------------------------------------
# Loading from pre-existing storage
# ---------------------------------------------------------------------------

class TestLoadFromStorage:

    def test_loads_existing_tasks(self):
        seed = Task("persisted", priority=Priority.HIGH)
        storage = FakeStorage(initial_tasks=[seed])
        manager = TaskManager(storage)
        assert len(manager.get_all_tasks()) == 1
        assert manager.get_task(seed.id).title == "persisted"
