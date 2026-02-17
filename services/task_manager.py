from models.task import Task
from models.enum import Priority


class TaskManager:

    def __init__(self,storage):
        self.storage = storage
        tasks = self.storage.load_tasks()
        self.tasks = {
            task.id : task
            for task in tasks
        }

    def _save(self):
        self.storage.save_tasks(self.tasks.values())


    def add_task(self,title,description=None,priority=Priority.MEDIUM):
        task = Task(title, description, priority)
        self.tasks[task.id] = task
        self._save()
        return task
    
    def get_task(self,task_id):
        try:
            return self.tasks[task_id]
        except KeyError:
            raise KeyError("Task does not exist")
    
    def delete_task(self, task_id):
            try:
                del self.tasks[task_id]
                self._save()
            except KeyError:
                raise KeyError("Task does not exist")

    def complete_task(self, task_id):
        task = self.get_task(task_id)
        task.mark_completed()
        self._save()

    def update_task(self, task_id, title=None, description=None, priority=None):
        task = self.get_task(task_id)

        if title is not None:
            task.update_title(title)

        if description is not None:
            task.update_description(description)

        if priority is not None:
            task.update_priority(priority)

        self._save()

    def get_all_tasks(self):
        return list(self.tasks.values())


        
