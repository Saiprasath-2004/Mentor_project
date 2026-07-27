from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class TeamBase(BaseModel):

    #Team display name
    name: str = Field(
        min_length=3,
        max_length=100
    )

    #optional description about the team 
    description: str | None = Field(
        default=None,
        max_length=255
    )

class TeamCreate(TeamBase):
    """
        Request schema used while creating a team.
        Owner is determined from the logged-in user,
        so client should not send owner_id.
    """
    pass

class TeamUpdate(TeamBase):
    # All fields optional for partial update 
    name: str | None  = Field(
        default=None,   
        min_length=3,
        max_length=100
    )

    description: str | None = Field(
        default=None,
        max_length=255
    )

class TeamResponse(TeamBase):
    id: UUID
    owner_id: UUID
    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )