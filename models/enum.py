from enum import Enum

class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"