from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.activity_schemas import ActivityResponse
from app.services.activity_service import ActivityService
from app.services.team_service import TeamService

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)

activity_service = ActivityService()
team_service = TeamService()


@router.get(
    "/teams/{team_id}",
    response_model=list[ActivityResponse]
)
async def list_team_activities(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Ensure the authenticated user owns the team
    await team_service.get_owned_team(
        db,
        team_id,
        current_user
    )

    return await activity_service.list_team_activity(
        db,
        team_id
    )