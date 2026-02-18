import argparse
from models.enum import Priority
from services.task_manager import TaskManager
from storage.json_storage import JsonStorage

def build_parser():

    parser = argparse.ArgumentParser(
        prog="task",
        description="CLI Task Manager"
    )

    subparsers = parser.add_subparsers(dest="command")

    # add command
    add = subparsers.add_parser("add", help="add a new task")
    add.add_argument("--title", help="title of the task")
    add.add_argument("--description", help="description of the task")
    add.add_argument("--priority", help="priority of the task", choices=["low","medium","high"])

    # list command 
    list = subparsers.add_parser("list", help="list all tasks")

    # get command
    get = subparsers.add_parser("get", help="get a task by id")
    get.add_argument("task_id", help="id of the task to retrieve")

    # sort command
    sort = subparsers.add_parser("sort", help="sort tasks by priority or created_at")
    sort.add_argument("sort", help="sort order by [priority, created_at]", choices=["priority","created_at"], default="created_at")

    # status command
    status_filter = subparsers.add_parser("status_filter", help="filter tasks by status")
    status_filter.add_argument("status", help="status to filter by", choices=["pending", "completed"])

    # update command
    update = subparsers.add_parser("update", help="update a task")
    update.add_argument("task_id", help="id of the task to update")
    update.add_argument("--title", help="new title of the task")
    update.add_argument("--description", help="new description of the task")
    update.add_argument("--priority", help="new priority of the task", choices=["low", "medium", "high"])
    
    # complete command
    complete = subparsers.add_parser("complete", help="mark a task as completed")
    complete.add_argument("task_id", help="id of the task to mark as completed")

    # delete command
    delete = subparsers.add_parser("delete", help="delete a task")
    delete.add_argument("task_id", help="id of the task to delete")

    return parser



def main():

    parser = build_parser()
    args = parser.parse_args()

    storage = JsonStorage("./data/tasks.json")
    manager = TaskManager(storage)


    if args.command == "add":

        priority = Priority[args.priority.upper()] if args.priority else Priority.MEDIUM

        task = manager.add_task(
            args.title,
            args.description,
            priority
        )

        print("🆕 Task created:", task.id)

    elif args.command == "get":

        try:
            print(f"{task.priority.value}  {task.status.value}")
            print(f"📌 {task.title}")
            print(f"🆔 {task.id}")
            print(f"{task.description}")
            print(end="\n")

        except KeyError:
            print("❌ Task not found:", args.task_id)

    elif args.command == "sort":
         
        tasks = manager.get_all_tasks()

        if args.sort == "priority":
              tasks.sort(key=lambda x:x.priority.value)

              for task in tasks:
                print(f"{task.priority.value}  {task.status.value}")
                print(f"📌 {task.title}")
                print(f"🆔 {task.id}")
                print(f"{task.description}")
                print(end="\n")

        elif args.sort == "created_at":
             tasks.sort(key=lambda x:x.created_at)

             for task in tasks:
                print(f"{task.priority.value}  {task.status.value}")
                print(f"📌 {task.title}")
                print(f"🆔 {task.id}")
                print(f"{task.description}")
                print(end="\n")
             

    elif args.command == "status_filter":
        tasks = manager.get_all_tasks()

        # print(len(tasks))

        if args.status == "pending":
            filtered_tasks = [task for task in tasks if task.status.value == "⏳ pending"]

            # print(len(filtered_tasks))
            

            for task in filtered_tasks:
                print(f"{task.priority.value}  {task.status.value}")
                print(f"📌 {task.title}")
                print(f"🆔 {task.id}")
                print(f"{task.description}")
                print(end="\n")

        elif args.status == "completed":
            filtered_tasks = [task for task in tasks if task.status.value == "✅ completed"]

            for task in filtered_tasks:
                print(f"{task.priority.value}  {task.status.value}")
                print(f"📌 {task.title}")
                print(f"🆔 {task.id}")
                print(f"{task.description}")
                print(end="\n")

    elif args.command == "list":

        tasks = manager.get_all_tasks()

        print(f"📋 Total tasks: {len(tasks)}\n")

        if not tasks:
            print("📋 No tasks found.")

        for task in tasks:
            print(f"{task.priority.value}  {task.status.value}")
            print(f"📌 {task.title}")
            print(f"🆔 {task.id}")
            print(f"{task.description}")
            print(end="\n")

        

    elif args.command == "update":
         
         priority = Priority[args.priority.upper()] if args.priority else Priority.MEDIUM
         manager.update_task(
              args.task_id,
              args.title,
              args.description,
              priority
         )

         print("✏️ Task updated")

    elif args.command == "complete":
         manager.complete_task(args.task_id)
         print("✅ Task marked as completed")

    elif args.command == "delete":
            manager.delete_task(args.task_id)
            print("🗑️ Task deleted")

    else:
         parser.print_help()

if __name__ == "__main__":
     main()