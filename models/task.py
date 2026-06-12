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

    @property   
    def id(self):
        return str(self._id)
    
    @property    
    def status(self):
        return self._status
    
    @property    
    def priority(self):
        return self._priority
    
    @property    
    def created_at(self):
        return self._created_at
    
    @property
    def completed_at(self):
        return self._completed_at.isoformat() if self._completed_at else None
    
    @property
    def is_completed(self):
        return self._status == Status.COMPLETED



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
        required_keys = ("id", "title", "status", "priority", "created_at", "updated_at")
        missing = [k for k in required_keys if k not in data]
        if missing:
            raise ValueError(f"Task data is missing required fields: {', '.join(missing)}")

        try:
            priority = Priority[data["priority"]]
        except KeyError:
            raise ValueError(
                f"Invalid priority '{data['priority']}'. "
                f"Expected one of: {', '.join(p.name for p in Priority)}"
            )

        try:
            status = Status[data["status"]]
        except KeyError:
            raise ValueError(
                f"Invalid status '{data['status']}'. "
                f"Expected one of: {', '.join(s.name for s in Status)}"
            )

        task = cls(
            title = data["title"],
            description = data.get("description"),
            priority=priority
        )

        try:
            task._id = uuid.UUID(data["id"])
        except ValueError:
            raise ValueError(f"Invalid task ID '{data['id']}': not a valid UUID")

        task._status = status

        try:
            task._created_at = datetime.fromisoformat(data["created_at"])
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid created_at timestamp: {e}")

        try:
            task._updated_at = datetime.fromisoformat(data["updated_at"])
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid updated_at timestamp: {e}")

        completed_at = data.get("completed_at")
        if completed_at:
            try:
                task._completed_at = datetime.fromisoformat(completed_at)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid completed_at timestamp: {e}")
        else:
            task._completed_at = None

        return task   
