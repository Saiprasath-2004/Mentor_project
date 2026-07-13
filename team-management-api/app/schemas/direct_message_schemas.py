from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DirectMessageCreate(BaseModel):
    message: str


class DirectMessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID

    sender_id: UUID
    sender_name: str

    message: str

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )