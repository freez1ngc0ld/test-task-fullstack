from enum import Enum


class StatusType(str, Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class PriorityType(str, Enum):
    LOW = 'low'
    NORMAL = 'normal'
    HIGH = 'high'


class AdminType(str, Enum):
    DEFAULTADMIN = 'defaultadmin'
    SUPERADMIN = 'superadmin'