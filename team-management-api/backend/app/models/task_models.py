import uuid
from datetime import datetime, timezone

from sqlalchemy import(
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    String,
    Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import TaskPriority,TaskStatus
from app.models.base import Base

class Task(Base):
    __tablename__ = "tasks"

    #Unique task Identifier
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    #task title
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    #Detailed description
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    #Current Task Status
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus),
        default=TaskStatus.TODO,
        nullable=False   
    )

    # Task priority
    priority: Mapped[TaskPriority] = mapped_column(
        SQLEnum(TaskPriority),
        default=TaskPriority.MEDIUM,
        nullable=False
    )

    #Team owning this task
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    #User assigned to work on the task
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # User who created the task
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # deadline
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    #Relationship
    team = relationship(
        "Team",
        back_populates="tasks"
    )


    assignee = relationship(
        "User",
        foreign_keys=[assigned_to],
        back_populates="assigned_tasks"
    )

    creator = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="created_tasks"
    )

    # Activity history for this task
    activities = relationship(
        "Activity",
        back_populates="task",
        cascade="all, delete-orphan"
    )
