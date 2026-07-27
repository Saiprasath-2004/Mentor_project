from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.activity_model import Activity

class ActivityRepository:

    #Persist a new activity event
    async def create_activity(
        self,
        db: AsyncSession,
        activity: Activity
    ) -> Activity:
        
        db.add(activity)
        await db.commit()
        await db.refresh(activity)

        return activity
        
    #Return all activities for a team 
    async def get_team_activities(
            self,
            db:AsyncSession,
            team_id: UUID
    )   -> list[Activity]:
        
        query = (
            select(Activity)
            .options(
                selectinload(Activity.user),
                selectinload(Activity.task)
            )
            .where(Activity.team_id == team_id)
            .order_by(Activity.created_at.desc())
        )

        result = await db.execute(query)

        return result.scalars().all()
        