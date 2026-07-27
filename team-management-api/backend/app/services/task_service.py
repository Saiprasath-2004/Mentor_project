from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.task_models import Task
from app.repository.task_repository import TaskRepository
from app.repository.team_repository import TeamRepository
from app.repository.team_member_repository import TeamMemberRepository
from app.schemas.task_schemas import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    TaskStatusUpdate
)
from app.services.activity_service import ActivityService
from app.core.enums import ActivityAction

class TaskService:

    def __init__(self):
        self.task_repo = TaskRepository()
        self.team_repo = TeamRepository()
        self.member_repo = TeamMemberRepository()
        self.activity_service = ActivityService()

    async def get_owned_task(
        self,
        db: AsyncSession,
        task_id: UUID,
        current_user: User
    ) -> Task:
        """
        Fetch a task only if it exists and the authenticated
        user owns the team that the task belongs to.

        Centralizing this logic keeps authorization consistent
        across all task operations.
        """

        task = await self.task_repo.get_task_by_id(
            db,
            task_id
        )

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found."
            )

        if task.team.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this task."
            )

        return task

    # Create a new task inside a team
    async def create_task(
        self,
        db: AsyncSession,
        team_id: UUID,
        task_data: TaskCreate,
        current_user: User
    ) -> TaskResponse:

        team = await self.team_repo.get_team_by_id(
            db,
            team_id
        )

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found."
            )

        if team.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the team owner can create tasks."
            )

        # Validate assigned user belongs to this team
        if task_data.assigned_to:

            member = await self.member_repo.get_member(
                db,
                team_id,
                task_data.assigned_to
            )

            if not member:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assigned user is not a member of this team."
                )

        task = Task(
            title=task_data.title,
            description=task_data.description,
            priority=task_data.priority,
            due_date=task_data.due_date,
            assigned_to=task_data.assigned_to,
            team_id=team_id,
            created_by=current_user.id
        )

        task = await self.task_repo.create_task(
            db,
            task
        )

        await self.activity_service.create_activity(
            db=db,
            team_id=team_id,
            user_id=current_user.id,
            task_id=task.id,
            action=ActivityAction.TASK_CREATED,
            description=f'Created task "{task.title}"'
        )

        return TaskResponse.model_validate(task)

    # Return all tasks belonging to a specific team
    async def list_tasks(
        self,
        db: AsyncSession,
        team_id: UUID,
        current_user: User
    ) -> list[TaskResponse]:

        team = await self.team_repo.get_team_by_id(
            db,
            team_id
        )

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found."
            )

        if team.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view these tasks."
            )

        tasks = await self.task_repo.get_team_tasks(
            db,
            team_id
        )

        return [
            TaskResponse.model_validate(task)
            for task in tasks
        ]

    # Return a single task after ownership validation
    async def get_task(
        self,
        db: AsyncSession,
        task_id: UUID,
        current_user: User
    ) -> TaskResponse:

        task = await self.get_owned_task(
            db,
            task_id,
            current_user
        )

        return TaskResponse.model_validate(task)

    # Update only the fields provided by the client
    async def update_task(
        self,
        db: AsyncSession,
        task_id: UUID,
        task_data: TaskUpdate,
        current_user: User
    ) -> TaskResponse:

        task = await self.get_owned_task(
            db,
            task_id,
            current_user
        )

        updates = task_data.model_dump(
            exclude_unset=True
        )

        # Validate newly assigned user belongs to the same team
        if (
            "assigned_to" in updates
            and updates["assigned_to"] is not None
        ):
            member = await self.member_repo.get_member(
                db,
                task.team_id,
                updates["assigned_to"]
            )

            if not member:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Assigned user is not a member of this team."
                )

        # Update only supplied fields
        for field, value in updates.items():
            setattr(task, field, value)

        updated_task = await self.task_repo.update_task(
            db,
            task
        )

        await self.activity_service.create_activity(
            db=db,
            team_id=task.team_id,
            user_id=current_user.id,
            task_id=task.id,
            action=ActivityAction.TASK_UPDATED,
            description=f'Updated task "{task.title}"'
        )

        return TaskResponse.model_validate(updated_task)

    # Update only the task workflow status
    async def update_status(
        self,
        db: AsyncSession,
        task_id: UUID,
        status_data: TaskStatusUpdate,
        current_user: User
    ) -> TaskResponse:

        task = await self.get_owned_task(
            db,
            task_id,
            current_user
        )

        task.status = status_data.status

        updated_task = await self.task_repo.update_task(
            db,
            task
        )

        await self.activity_service.create_activity(
            db=db,
            team_id=task.team_id,
            user_id=current_user.id,
            task_id=task.id,
            action=ActivityAction.TASK_STATUS_UPDATED,
            description=f'Changed task status to {task.status.value}'
        )

        return TaskResponse.model_validate(updated_task)

    # Permanently delete a task
    async def delete_task(
        self,
        db: AsyncSession,
        task_id: UUID,
        current_user: User
    ) -> None:

        task = await self.get_owned_task(
            db,
            task_id,
            current_user
        )

        await self.activity_service.create_activity(
            db=db,
            team_id=task.team_id,
            user_id=current_user.id,
            task_id=task.id,
            action=ActivityAction.TASK_DELETED,
            description=f'Deleted task "{task.title}"'
        )

        await self.task_repo.delete_task(
            db,
            task
        )