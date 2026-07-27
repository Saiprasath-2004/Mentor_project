from uuid import UUID

from fastapi import APIRouter, Depends
from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.schemas.team_schemas import TeamCreate, TeamResponse, TeamUpdate
from app.models.user import User
from app.services.team_service import TeamService
from app.services.task_service import TaskService
from app.schemas.task_schemas import (
    TaskCreate,
    TaskResponse,
)

router =APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

team_service = TeamService()
task_service = TaskService()

#Create a team for the currently authenticated user
@router.post(
    "",
    response_model=TeamResponse,
    status_code=201
)
async def create_team( team_data: TeamCreate,
                       db: AsyncSession = Depends(get_db),
                       current_user: User = Depends(get_current_user)):
    return await team_service.create_team(
        db,
        team_data,
        current_user
    )



# Return all teams created by the authenticated user
@router.get(
    "",
    response_model=list[TeamResponse]
)
async def get_my_teams( db:AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    return await team_service.get_my_teams(
        db,
        current_user
    )


@router.get("/{team_id}",response_model=TeamResponse)
async def get_team(team_id: UUID,
                   db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    return await team_service.get_team(
        db,
        team_id,
        current_user
    )

@router.put("/{team_id}",response_model=TeamResponse)
async def update_team(team_id: UUID,
                      team_data: TeamUpdate,
                      db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(get_current_user)
):
    return await team_service.update_team(
        db,
        team_id,
        team_data,
        current_user
    )

@router.delete("/{team_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(team_id: UUID,
                     db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):

            await team_service.delete_team(
                  db,
                  team_id,
                  current_user

            )

# ------------------------------------------------------------------
# Create a task inside a team
# ------------------------------------------------------------------
@router.post(
    "/{team_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_task(
    team_id: UUID,
    task_data: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.create_task(
        db,
        team_id,
        task_data,
        current_user
    )


# ------------------------------------------------------------------
# Return every task belonging to a team
# ------------------------------------------------------------------
@router.get(
    "/{team_id}/tasks",
    response_model=list[TaskResponse]
)
async def list_tasks(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.list_tasks(
        db,
        team_id,
        current_user
    )

