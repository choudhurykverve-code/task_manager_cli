import json
import os
import sys
from pathlib import Path
from models.task import Task


class JsonStorage:

    def __init__(self, path):
        self.filepath = path

    def save_tasks(self, tasks):
        data = [task.to_dict() for task in tasks]

        fd = os.open(self.filepath, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=4)
        except Exception:
            os.close(fd)
            raise
        os.chmod(self.filepath, 0o600)

    def load_tasks(self):
        path = Path(self.filepath)

        if not path.exists():
            return []

        try:
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                tasks = [Task.from_dict(item) for item in data]
                return tasks

        except json.JSONDecodeError:
            print(
                "WARNING: Task data file is corrupted. "
                "Please check or restore: " + self.filepath,
                file=sys.stderr,
            )
            return []

        except PermissionError:
            print(
                "ERROR: Permission denied reading task file: " + self.filepath,
                file=sys.stderr,
            )
            return []
