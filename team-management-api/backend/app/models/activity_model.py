import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import ActivityAction
from app.models.base import Base


class Activity(Base):
    __tablename__ = "activities"

    #Unique activity identifier
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    #Team where the activity occured
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # User who performed the action
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Related task (optional)
    task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Business event
    action: Mapped[ActivityAction] = mapped_column(
        SQLEnum(ActivityAction),
        nullable=False
    )

    # Human-readable description
    description: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    # Event timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    team = relationship(
        "Team",
        back_populates="activities"
    )

    user = relationship(
        "User",
        back_populates="activities"
    )

    task = relationship(
        "Task",
        back_populates="activities"
    )
