import sys
import pytest

from task_cli import build_parser


class TestBuildParser:
    """Verify that the argparse parser accepts the documented CLI forms."""

    def test_add_all_flags(self):
        parser = build_parser()
        args = parser.parse_args(["add", "--title", "T", "--description", "D", "--priority", "high"])
        assert args.command == "add"
        assert args.title == "T"
        assert args.description == "D"
        assert args.priority == "high"

    def test_add_title_only(self):
        parser = build_parser()
        args = parser.parse_args(["add", "--title", "T"])
        assert args.command == "add"
        assert args.title == "T"
        assert args.description is None
        assert args.priority is None

    def test_list(self):
        parser = build_parser()
        args = parser.parse_args(["list"])
        assert args.command == "list"

    def test_get(self):
        parser = build_parser()
        args = parser.parse_args(["get", "some-id"])
        assert args.command == "get"
        assert args.task_id == "some-id"

    def test_complete(self):
        parser = build_parser()
        args = parser.parse_args(["complete", "some-id"])
        assert args.command == "complete"
        assert args.task_id == "some-id"

    def test_delete(self):
        parser = build_parser()
        args = parser.parse_args(["delete", "some-id"])
        assert args.command == "delete"
        assert args.task_id == "some-id"

    def test_update_all_flags(self):
        parser = build_parser()
        args = parser.parse_args(["update", "id", "--title", "T", "--description", "D", "--priority", "low"])
        assert args.command == "update"
        assert args.task_id == "id"
        assert args.title == "T"
        assert args.description == "D"
        assert args.priority == "low"

    def test_sort_priority(self):
        parser = build_parser()
        args = parser.parse_args(["sort", "priority"])
        assert args.command == "sort"
        assert args.sort == "priority"

    def test_sort_created_at(self):
        parser = build_parser()
        args = parser.parse_args(["sort", "created_at"])
        assert args.sort == "created_at"

    def test_status_filter_pending(self):
        parser = build_parser()
        args = parser.parse_args(["status_filter", "pending"])
        assert args.command == "status_filter"
        assert args.status == "pending"

    def test_status_filter_completed(self):
        parser = build_parser()
        args = parser.parse_args(["status_filter", "completed"])
        assert args.status == "completed"

    def test_invalid_priority_rejected(self):
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["add", "--priority", "critical"])

    def test_no_command_gives_none(self):
        parser = build_parser()
        args = parser.parse_args([])
        assert args.command is None
