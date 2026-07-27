from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.core.enums import ActivityAction

class ActivityResponse(BaseModel):
    #Response returned for an activity event

    id: UUID
    team_id: UUID
    user_id: UUID | None
    task_id: UUID | None
    action: ActivityAction
    description: str
    created_at : datetime
    
    model_config = ConfigDict(
        from_attributes=True
    )