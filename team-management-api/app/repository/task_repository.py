from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.task_models import Task

class TaskRepository:

    # Create a new task
    async def create_task(
        self,
        db: AsyncSession,
        task: Task
    )  -> Task:
        db.add(task)
        await db.commit()
        await db.refresh(task)

        return task
    
    #Fetch task using its unique ID
    async def get_task_by_id(
        self,
        db: AsyncSession,
        task_id: UUID    
    ) -> Task | None:
        
        query = (select(Task)
                .options(
                    selectinload(Task.team)
                )
                .where(Task.id == task_id))

        result = await db.execute(query)
        return result.scalar_one_or_none()

    #Return every task belonging to a team
    async def get_team_tasks(
        self,
        db: AsyncSession,
        team_id: UUID
    ) -> list[Task]:
        query = (select(Task)
                 .options(
                    selectinload(Task.team)
                )
                .where(Task.team_id == team_id))

        result = await db.execute(query)

        return result.scalars().all()
    
    # Persist update task
    async def update_task(
        self,
        db: AsyncSession,
        task:Task
    ) -> Task:
        
        await db.commit()
        await db.refresh(task)

        return task
    
    #Permanently delete task
    async def delete_task(
        self,
        db: AsyncSession,
        task:Task
    )  -> None:
        await db.delete(task)
        await db.commit()

        

