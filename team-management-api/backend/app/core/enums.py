from enum import Enum

class TeamRole(str, Enum):
    """
        Roles assigned to members inside a team.

        Note:
        Team owner is NOT stored here.
        Ownership is determined by teams.owner_id.
    """

    ADMIN = "ADMIN"
    MEMBER = "MEMBER"


class TaskStatus(str, Enum):
    """
    Current progress of a task.
    """

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"

class TaskPriority(str, Enum):
    """
    Importance of a task.
    """

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ActivityAction(str, Enum):
    """
    Represents a business event performed in the system.
    """

    TASK_CREATED = "TASK_CREATED"
    TASK_UPDATED = "TASK_UPDATED"
    TASK_STATUS_UPDATED = "TASK_STATUS_UPDATED"
    TASK_DELETED = "TASK_DELETED"
    MEMBER_ADDED = "MEMBER_ADDED"
    MEMBER_REMOVED = "MEMBER_REMOVED"
    TEAM_CREATED = "TEAM_CREATED"
    TEAM_UPDATED = "TEAM_UPDATED"
    TEAM_DELETED = "TEAM_DELETED"
