import json
import sys
from pathlib import Path
from models.task import Task


class JsonStorage:

    def __init__(self, path):
        self.filepath = path

    def save_tasks(self, tasks):
        data = [task.to_dict() for task in tasks]

        path = Path(self.filepath)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(
                f"Cannot create directory '{path.parent}': {e}"
            ) from e

        try:
            with open(self.filepath, "w") as f:
                json.dump(data, f, indent=4)
        except PermissionError as e:
            raise PermissionError(
                f"Permission denied writing to '{self.filepath}': {e}"
            ) from e
        except OSError as e:
            raise OSError(
                f"Failed to save tasks to '{self.filepath}': {e}"
            ) from e

    def load_tasks(self):
        path = Path(self.filepath)

        if not path.exists():
            return []

        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(
                f"Warning: Task file '{self.filepath}' contains invalid JSON "
                f"and could not be loaded: {e}",
                file=sys.stderr,
            )
            return []
        except PermissionError as e:
            print(
                f"Warning: Permission denied reading '{self.filepath}': {e}",
                file=sys.stderr,
            )
            return []

        tasks = []
        for i, item in enumerate(data):
            try:
                tasks.append(Task.from_dict(item))
            except (KeyError, ValueError, TypeError) as e:
                print(
                    f"Warning: Skipping corrupted task entry {i}: {e}",
                    file=sys.stderr,
                )
        return tasks
