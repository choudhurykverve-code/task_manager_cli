import argparse
import os
import sys
import uuid
from models.enum import Priority
from services.task_manager import TaskManager
from storage.json_storage import JsonStorage


def validate_task_id(value):
    """Validate that the task_id is a well-formed UUID."""
    try:
        uuid.UUID(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid task ID: {value!r}")
    return value


def build_parser():

    parser = argparse.ArgumentParser(
        prog="task",
        description="CLI Task Manager"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", help="add a new task")
    add.add_argument("--title", required=True, help="title of the task")
    add.add_argument("--description", help="description of the task")
    add.add_argument("--priority", help="priority of the task", choices=["low", "medium", "high"])

    subparsers.add_parser("list", help="list all tasks")

    get = subparsers.add_parser("get", help="get a task by id")
    get.add_argument("task_id", type=validate_task_id, help="id of the task to retrieve")

    sort = subparsers.add_parser("sort", help="sort tasks by priority or created_at")
    sort.add_argument("sort", help="sort order by [priority, created_at]", choices=["priority", "created_at"], default="created_at")

    status_filter = subparsers.add_parser("status_filter", help="filter tasks by status")
    status_filter.add_argument("status", help="status to filter by", choices=["pending", "completed"])

    update = subparsers.add_parser("update", help="update a task")
    update.add_argument("task_id", type=validate_task_id, help="id of the task to update")
    update.add_argument("--title", help="new title of the task")
    update.add_argument("--description", help="new description of the task")
    update.add_argument("--priority", help="new priority of the task", choices=["low", "medium", "high"])

    complete = subparsers.add_parser("complete", help="mark a task as completed")
    complete.add_argument("task_id", type=validate_task_id, help="id of the task to mark as completed")

    delete = subparsers.add_parser("delete", help="delete a task")
    delete.add_argument("task_id", type=validate_task_id, help="id of the task to delete")

    return parser


def _print_task(task):
    print(f"\n{task.priority.value}  {task.status.value}")
    print(f"Title: {task.title}")
    print(f"Task ID: {task.id}")
    print(f"Description: {task.description}")
    print()


def main():

    parser = build_parser()
    args = parser.parse_args()

    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    storage = JsonStorage(os.path.join(data_dir, "tasks.json"))
    manager = TaskManager(storage)

    if args.command == "add":

        priority = Priority[args.priority.upper()] if args.priority else Priority.MEDIUM

        try:
            task = manager.add_task(
                args.title,
                args.description,
                priority
            )
            print("Task created Successfully:", task.id)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "get":

        try:
            task = manager.get_task(args.task_id)
            _print_task(task)
        except KeyError:
            print("Task not found:", args.task_id)
            sys.exit(1)

    elif args.command == "sort":

        tasks = manager.get_all_tasks()

        if args.sort == "priority":
            PRIORITY_ORDER = {
                "HIGH": 1,
                "MEDIUM": 2,
                "LOW": 3
            }
            tasks.sort(key=lambda x: PRIORITY_ORDER[x.priority.value])

        elif args.sort == "created_at":
            tasks.sort(key=lambda x: x.created_at)

        for task in tasks:
            _print_task(task)

    elif args.command == "status_filter":
        tasks = manager.get_all_tasks()
        status_value = args.status.upper()
        filtered_tasks = [task for task in tasks if task.status.value == status_value]

        for task in filtered_tasks:
            _print_task(task)

    elif args.command == "list":

        tasks = manager.get_all_tasks()

        print(f"Total tasks: {len(tasks)}\n")

        if not tasks:
            print("No tasks found.")

        for task in tasks:
            _print_task(task)

    elif args.command == "update":

        priority = Priority[args.priority.upper()] if args.priority else None

        try:
            manager.update_task(
                args.task_id,
                args.title,
                args.description,
                priority
            )
            print("Task updated Successfully")
        except KeyError:
            print("Task not found:", args.task_id, file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "complete":
        try:
            manager.complete_task(args.task_id)
            print("Task marked as completed")
        except KeyError:
            print("Task not found:", args.task_id, file=sys.stderr)
            sys.exit(1)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "delete":
        try:
            manager.delete_task(args.task_id)
            print("Task deleted Successfully")
        except KeyError:
            print("Task not found:", args.task_id, file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
