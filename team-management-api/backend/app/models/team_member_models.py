import uuid
from datetime import datetime, timezone


from sqlalchemy import (
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import TeamRole
from app.models.base import Base


class TeamMember(Base):
    __tablename__ = "team_members"

    #Prevent duplicate memberships for the same user in a team
    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "user_id",
            name="uq_team_member"
        ),
    )

    # Unique membership ID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    # Team this membership belongs to 
    team_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # user who is a member of the team
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True

    )

    #Permission level inside team
    role: Mapped[TeamRole] = mapped_column(
        SQLEnum(TeamRole),
        default=TeamRole.MEMBER,
        nullable=False
    )

    #when the user joined the team 
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


    #ORM relationships
    team = relationship(
        "Team",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="team_members"
    )