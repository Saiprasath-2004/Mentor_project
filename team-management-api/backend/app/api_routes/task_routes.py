from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.models.user import User
from app.schemas.task_schemas import(
    TaskResponse,
    TaskStatusUpdate,
    TaskUpdate
)

from app.services.task_service import TaskService

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

task_service = TaskService()


@router.get(
    "/{task_id}",
    response_model=TaskResponse
)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.get_task(
        db,
        task_id,
        current_user
    )


@router.put(
    "/{task_id}",
    response_model=TaskResponse
)
async def update_task(
    task_id: UUID,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.update_task(
        db,
        task_id,
        task_data,
        current_user
    )


@router.patch(
    "/{task_id}/status",
    response_model=TaskResponse
)
async def update_status(
    task_id: UUID,
    status_data: TaskStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await task_service.update_status(
        db,
        task_id,
        status_data,
        current_user
    )

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await task_service.delete_task(
        db,
        task_id,
        current_user
    )