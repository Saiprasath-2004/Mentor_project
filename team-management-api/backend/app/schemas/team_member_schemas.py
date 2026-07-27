from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.core.enums import TeamRole



class TeamMemberCreate(BaseModel):
    # user to be added into the team 
    user_id: UUID

    #optional role while joining
    role: TeamRole = TeamRole.MEMBER

class TeamMemberResponse(BaseModel):
    id: UUID
    team_id: UUID
    user_id: UUID
    role: TeamRole

    model_config = ConfigDict(
        from_attributes=True
    )





































