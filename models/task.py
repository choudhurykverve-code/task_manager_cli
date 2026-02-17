import uuid
from models.enum import Status,Priority
from datetime import datetime,timezone

class Task:
    def __init__(self,title,description=None,priority=Priority.MEDIUM):

        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        
        if not isinstance(priority, Priority):
            raise ValueError("Priority must be a Priority enum.")
        
        self._id = uuid.uuid4()
        self.title = title.strip()
        self.description = description
        self._status = Status.PENDING
        self._priority = priority
        self._created_at = datetime.now(timezone.utc)
        self._updated_at = self._created_at
        self._completed_at = None


    def mark_completed(self):

        if self._status == Status.COMPLETED:
            raise ValueError("Task is already completed.")
            
        now = datetime.now(timezone.utc)
        self._status = Status.COMPLETED
        self._completed_at = now
        self._updated_at = now

    def update_title(self,title):
        if not title:
            raise ValueError("Title cannot be empty.")
        
        self.title = title
        self._updated_at = datetime.now(timezone.utc)


    def update_description(self,description):
        # if not description or description.strip():
        #     raise ValueError("Title cannot be empty.")
        
        self.description = description
        self._updated_at = datetime.now(timezone.utc)


    def update_priority(self,priority):
        if not isinstance(priority, Priority):
            raise ValueError("Priority can be only enum.")
        
        self._priority = priority
        self._updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "id":str(self._id),
            "title":self.title,
            "description":self.description,
            "status":self._status.name,
            "priority":self._priority.name,
            "created_at":self._created_at.isoformat(),
            "updated_at":self._updated_at.isoformat() if self._updated_at else None,
            "completed_at":self._completed_at.isoformat() if self._completed_at else None
        }
    
    @classmethod
    def from_dict(cls,data):
        task = cls(
            title = data["title"],
            description = data.get("description"),
            priority=Priority[data["priority"]]
        )

        task._id =  uuid.UUID(data["id"])
        task._status = Status[data["status"]]
        task._created_at = datetime.fromisoformat(data["created_at"])
        task._updated_at = datetime.fromisoformat(data["updated_at"])
        task._completed_at = (
            datetime.fromisoformat(data["completed_at"])
            if data["completed_at"]
            else None
        )

        return task   