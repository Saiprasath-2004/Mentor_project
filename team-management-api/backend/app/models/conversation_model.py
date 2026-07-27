from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


from app.models.base import Base

class Conversation(Base):

    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(
        UUID (as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    participants = relationship(
        "ConversationParticipant",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )

    messages = relationship(
        "DirectMessage",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )