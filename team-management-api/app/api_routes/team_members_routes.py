from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.team_member_schemas import(
    TeamMemberCreate,
    TeamMemberResponse
)
from app.services.team_member_service import TeamMemberService

router = APIRouter(
    prefix="/teams",
    tags=["Team Members"]
)

member_service = TeamMemberService()

@router.post(
    "/{team_id}/members",
    response_model=TeamMemberResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_member(
    team_id:UUID,
    member_data: TeamMemberCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await member_service.add_member(
        db,
        team_id,
        member_data,
        current_user
    )


@router.get(
    "/{team_id}/members",
    response_model=list[TeamMemberResponse]
)
async def list_members(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return await member_service.list_members(
        db,
        team_id,
        current_user
    )

@router.delete(
    "/{team_id}/members/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_member(
    team_id : UUID,
    user_id : UUID,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user)
):
    await member_service.remove_member(
        db,
        team_id,
        user_id,
        current_user
    )
