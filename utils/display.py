def format_task(task):
    """Format a single task for terminal display."""
    return (
        f"\n{task.priority.value}  {task.status.value}\n"
        f"Title: {task.title}\n"
        f"Task ID: {task.id}\n"
        f"Description: {task.description}\n"
    )


def print_task(task):
    """Print a single task to stdout."""
    print(format_task(task))


def print_task_list(tasks, empty_message="No tasks found."):
    """Print a list of tasks. Shows empty_message if list is empty."""
    if not tasks:
        print(empty_message)
        return

    for task in tasks:
        print_task(task)
