import uuid
from models.enum import Status, Priority
from datetime import datetime, timezone

MAX_TITLE_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 2000


class Task:
    def __init__(self, title, description=None, priority=Priority.MEDIUM):

        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")

        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title must be at most {MAX_TITLE_LENGTH} characters."
            )

        if description and len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description must be at most {MAX_DESCRIPTION_LENGTH} characters."
            )

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

    def update_title(self, title):
        if not title:
            raise ValueError("Title cannot be empty.")

        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError(
                f"Title must be at most {MAX_TITLE_LENGTH} characters."
            )

        self.title = title
        self._updated_at = datetime.now(timezone.utc)

    def update_description(self, description):
        if description and len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description must be at most {MAX_DESCRIPTION_LENGTH} characters."
            )

        self.description = description
        self._updated_at = datetime.now(timezone.utc)

    def update_priority(self, priority):
        if not isinstance(priority, Priority):
            raise ValueError("Priority can be only enum.")

        self._priority = priority
        self._updated_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            "id": str(self._id),
            "title": self.title,
            "description": self.description,
            "status": self._status.name,
            "priority": self._priority.name,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat() if self._updated_at else None,
            "completed_at": self._completed_at.isoformat() if self._completed_at else None
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            title=data["title"],
            description=data.get("description"),
            priority=Priority[data["priority"]]
        )

        task._id = uuid.UUID(data["id"])
        task._status = Status[data["status"]]
        task._created_at = datetime.fromisoformat(data["created_at"])
        task._updated_at = datetime.fromisoformat(data["updated_at"])
        task._completed_at = (
            datetime.fromisoformat(data["completed_at"])
            if data["completed_at"]
            else None
        )

        return task
