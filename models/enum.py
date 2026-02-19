from enum import Enum

class Status(Enum):
    PENDING = "pending"
    COMPLETED = "completed"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"