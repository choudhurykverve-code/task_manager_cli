"""Integration tests for the ``main()`` function in task_cli.py.

Each test patches ``sys.argv`` and uses a temporary JSON file so that
tests never touch the real ``data/tasks.json``.
"""

import json
import sys
from unittest import mock

import pytest

from task_cli import main


@pytest.fixture(autouse=True)
def _isolate_storage(tmp_path, monkeypatch):
    """Redirect JsonStorage to a temp file for every test."""
    tmp_json = str(tmp_path / "tasks.json")
    monkeypatch.setattr(
        "task_cli.JsonStorage",
        lambda _path: __import__("storage.json_storage", fromlist=["JsonStorage"]).JsonStorage(tmp_json),
    )


def _run(args: list[str], monkeypatch):
    monkeypatch.setattr(sys, "argv", ["task"] + args)
    main()


# ---------------------------------------------------------------------------
# add
# ---------------------------------------------------------------------------

class TestAddCommand:

    def test_add_prints_id(self, capsys, monkeypatch):
        _run(["add", "--title", "Buy milk"], monkeypatch)
        out = capsys.readouterr().out
        assert "Task created Successfully:" in out

    def test_add_with_priority(self, capsys, monkeypatch):
        _run(["add", "--title", "T", "--priority", "high"], monkeypatch)
        assert "Task created Successfully:" in capsys.readouterr().out


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------

class TestListCommand:

    def test_list_empty(self, capsys, monkeypatch):
        _run(["list"], monkeypatch)
        out = capsys.readouterr().out
        assert "Total tasks: 0" in out
        assert "No tasks found." in out

    def test_list_after_add(self, capsys, monkeypatch):
        _run(["add", "--title", "A"], monkeypatch)
        _run(["list"], monkeypatch)
        out = capsys.readouterr().out
        assert "Total tasks: 1" in out


# ---------------------------------------------------------------------------
# get
# ---------------------------------------------------------------------------

class TestGetCommand:

    def test_get_existing(self, capsys, monkeypatch):
        _run(["add", "--title", "Find me"], monkeypatch)
        add_out = capsys.readouterr().out
        task_id = add_out.split(":")[-1].strip()

        _run(["get", task_id], monkeypatch)
        out = capsys.readouterr().out
        assert "Find me" in out

    def test_get_missing(self, capsys, monkeypatch):
        _run(["get", "nonexistent"], monkeypatch)
        out = capsys.readouterr().out
        assert "Task not found" in out


# ---------------------------------------------------------------------------
# complete
# ---------------------------------------------------------------------------

class TestCompleteCommand:

    def test_complete(self, capsys, monkeypatch):
        _run(["add", "--title", "Do it"], monkeypatch)
        task_id = capsys.readouterr().out.split(":")[-1].strip()

        _run(["complete", task_id], monkeypatch)
        out = capsys.readouterr().out
        assert "Task marked as completed" in out


# ---------------------------------------------------------------------------
# update
# ---------------------------------------------------------------------------

class TestUpdateCommand:

    def test_update_title(self, capsys, monkeypatch):
        _run(["add", "--title", "Old"], monkeypatch)
        task_id = capsys.readouterr().out.split(":")[-1].strip()

        _run(["update", task_id, "--title", "New"], monkeypatch)
        out = capsys.readouterr().out
        assert "Task updated Successfully" in out


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------

class TestDeleteCommand:

    def test_delete(self, capsys, monkeypatch):
        _run(["add", "--title", "Gone"], monkeypatch)
        task_id = capsys.readouterr().out.split(":")[-1].strip()

        _run(["delete", task_id], monkeypatch)
        out = capsys.readouterr().out
        assert "Task deleted Successfully" in out


# ---------------------------------------------------------------------------
# sort
# ---------------------------------------------------------------------------

class TestSortCommand:

    def test_sort_by_priority(self, capsys, monkeypatch):
        _run(["add", "--title", "Low", "--priority", "low"], monkeypatch)
        _run(["add", "--title", "High", "--priority", "high"], monkeypatch)
        capsys.readouterr()  # clear

        _run(["sort", "priority"], monkeypatch)
        out = capsys.readouterr().out
        # HIGH should appear before LOW in output
        assert out.index("HIGH") < out.index("LOW")

    def test_sort_by_created_at(self, capsys, monkeypatch):
        _run(["add", "--title", "First"], monkeypatch)
        _run(["add", "--title", "Second"], monkeypatch)
        capsys.readouterr()

        _run(["sort", "created_at"], monkeypatch)
        out = capsys.readouterr().out
        assert "First" in out
        assert "Second" in out


# ---------------------------------------------------------------------------
# status_filter
# ---------------------------------------------------------------------------

class TestStatusFilterCommand:

    def test_filter_pending(self, capsys, monkeypatch):
        _run(["add", "--title", "Pending task"], monkeypatch)
        capsys.readouterr()

        _run(["status_filter", "pending"], monkeypatch)
        out = capsys.readouterr().out
        assert "Pending task" in out

    def test_filter_completed(self, capsys, monkeypatch):
        _run(["add", "--title", "Will complete"], monkeypatch)
        task_id = capsys.readouterr().out.split(":")[-1].strip()

        _run(["complete", task_id], monkeypatch)
        capsys.readouterr()

        _run(["status_filter", "completed"], monkeypatch)
        out = capsys.readouterr().out
        assert "Will complete" in out


# ---------------------------------------------------------------------------
# no command → help
# ---------------------------------------------------------------------------

class TestNoCommand:

    def test_no_args_prints_help(self, capsys, monkeypatch):
        _run([], monkeypatch)
        out = capsys.readouterr().out
        assert "CLI Task Manager" in out
