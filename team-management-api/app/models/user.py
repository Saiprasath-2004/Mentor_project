from uuid import uuid4
from datetime import datetime, timezone

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):

    __tablename__ = "users"

    # Unique user identifier (better than sequential integer IDs)
    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=lambda:uuid4()
    )

    # Indexed for faster login/email lookup
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Stores hashed password, never plain password
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    # Used later for email verification flow
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    # Stores account creation timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc)
    )