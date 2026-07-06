from datetime import datetime, timezone
import  uuid

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

class Team(Base):
    __tablename__ = "teams"

    #Unique identifier for eachteam
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    #Display name of the team 
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # optional description about the team's purpose
    description: Mapped[str] = mapped_column(
        String(255),
        nullable= True
    )

    # User who owns this team
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )


    #Timestamp when the team was created
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    ##orm relationship to access team owner
    owner = relationship(
        "User",
        back_populates="teams"
    )