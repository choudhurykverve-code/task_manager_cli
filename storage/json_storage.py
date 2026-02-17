import json
from pathlib import Path
from models.task import  Task

class JsonStorage:

    def __init__(self, path):
        self.filepath = path

    def save_tasks(self,tasks):
        data = [task.to_dict() for task in tasks]

        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)


    def load_tasks(self):
        path = Path(self.filepath)

        if not path.exists():
            return []
        
        try:

            with open(self.filepath,'r') as f:

                data = json.load(f)
                tasks = [Task.from_dict(item) for item in data]

                return tasks

        except (json.JSONDecodeError, PermissionError):
            return []






