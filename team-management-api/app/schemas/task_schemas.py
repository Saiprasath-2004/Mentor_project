from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.core.enums import(
    TaskPriority,
    TaskStatus
)

class TaskCreate(BaseModel):
    # Request schema for creating a task.

    title: str= Field(
        min_length=3,
        max_length=200
    )

    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    assigned_to: UUID | None = None
    due_date: datetime | None = None

class  TaskUpdate(BaseModel):
    #Request schemas for updating task details.

    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=200
    )

    description: str | None = None
    priority : TaskPriority | None = None
    assigned_to: UUID | None = None
    due_date : datetime | None = None

class TaskStatusUpdate(BaseModel):

    #Update only task status
    status: TaskStatus

class TaskResponse(BaseModel):
    #Task Response returned to a client

    id: UUID
    title: str
    description: str |None
    status: TaskStatus
    priority: TaskPriority
    team_id: UUID
    assigned_to: UUID | None
    created_by: UUID
    due_date: datetime | None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )