import argparse
from services.task_manager import TaskManager
from storage.json_storage import JsonStorage
from utils.display import print_task, print_task_list
from utils.parsers import parse_priority
from utils.sorting import sort_by_priority, sort_by_created_at

def build_parser():

    parser = argparse.ArgumentParser(
        prog="task",
        description="CLI Task Manager"
    )

    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser("add", help="add a new task")
    add.add_argument("--title", help="title of the task")
    add.add_argument("--description", help="description of the task")
    add.add_argument("--priority", help="priority of the task", choices=["low","medium","high"])

    list = subparsers.add_parser("list", help="list all tasks")

    get = subparsers.add_parser("get", help="get a task by id")
    get.add_argument("task_id", help="id of the task to retrieve")

    sort = subparsers.add_parser("sort", help="sort tasks by priority or created_at")
    sort.add_argument("sort", help="sort order by [priority, created_at]", choices=["priority","created_at"], default="created_at")

    status_filter = subparsers.add_parser("status_filter", help="filter tasks by status")
    status_filter.add_argument("status", help="status to filter by", choices=["pending", "completed"])

    update = subparsers.add_parser("update", help="update a task")
    update.add_argument("task_id", help="id of the task to update")
    update.add_argument("--title", help="new title of the task")
    update.add_argument("--description", help="new description of the task")
    update.add_argument("--priority", help="new priority of the task", choices=["low", "medium", "high"])
    
    complete = subparsers.add_parser("complete", help="mark a task as completed")
    complete.add_argument("task_id", help="id of the task to mark as completed")

    delete = subparsers.add_parser("delete", help="delete a task")
    delete.add_argument("task_id", help="id of the task to delete")

    return parser



def main():

    parser = build_parser()
    args = parser.parse_args()

    storage = JsonStorage("./data/tasks.json")
    manager = TaskManager(storage)


    if args.command == "add":

        priority = parse_priority(args.priority)

        task = manager.add_task(
            args.title,
            args.description,
            priority
        )

        print("Task created Successfully:", task.id)

    elif args.command == "get":

        try:
            task = manager.get_task(args.task_id)
            print_task(task)

        except KeyError:
            print("Task not found:", args.task_id)

    elif args.command == "sort":
         
        tasks = manager.get_all_tasks()

        if args.sort == "priority":
            sorted_tasks = sort_by_priority(tasks)
        else:
            sorted_tasks = sort_by_created_at(tasks)

        print_task_list(sorted_tasks)

    elif args.command == "status_filter":
        tasks = manager.get_all_tasks()
        filtered_tasks = [
            task for task in tasks
            if task.status.value == args.status.upper()
        ]
        print_task_list(filtered_tasks)

    elif args.command == "list":

        tasks = manager.get_all_tasks()

        print(f"Total tasks: {len(tasks)}\n")
        print_task_list(tasks)

    elif args.command == "update":
         
         priority = parse_priority(args.priority)
         manager.update_task(
              args.task_id,
              args.title,
              args.description,
              priority
         )

         print("Task updated Successfully")

    elif args.command == "complete":
         manager.complete_task(args.task_id)
         print("Task marked as completed")

    elif args.command == "delete":
            manager.delete_task(args.task_id)
            print("Task deleted Successfully")

    else:
         parser.print_help()

if __name__ == "__main__":
     main()
