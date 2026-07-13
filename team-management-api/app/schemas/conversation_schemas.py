from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConversationResponse(BaseModel):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ConversationListResponse(BaseModel):
    id: UUID
    other_user_id: UUID
    other_username: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )