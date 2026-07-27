from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import ActivityAction
from app.core.sse_manager import sse_manager
from app.models.activity_model import Activity
from app.repository.activity_repository import ActivityRepository
from app.schemas.activity_schemas import ActivityResponse

class ActivityService:

    def __init__(self):
        self.activity_repo = ActivityRepository()

    #Create new activity
    async def create_activity(
        self,
        db:AsyncSession,
        team_id: UUID,
        user_id: UUID,
        action: ActivityAction,
        description: str,
        task_id: UUID | None = None
    ):
        activity = Activity(

            team_id=team_id,
            user_id=user_id,
            task_id=task_id,
            action=action,
            description=description
        )

        await self.activity_repo.create_activity(
            db,
            activity
        )

        await sse_manager.broadcast(
            activity.team_id,
            {
                "id": str(activity.id),
                "team_id" : str(activity.team_id),
                "user_id" : str(activity.user_id) if activity.user_id else None,
                "task_id" : str(activity.task_id) if activity.task_id else None,
                "action" :  activity.action.value,
                "description" : activity.description,
                "created_at" : activity.created_at.isoformat(),
            }
        )

    #Return activity timeline for a team
    async def list_team_activity(
        self,
        db: AsyncSession,
        team_id: UUID
    ) -> list[ActivityResponse]:
        
        activities = await self.activity_repo.get_team_activities(
            db,
            team_id
        )

        return [
            ActivityResponse.model_validate(activity)
            for activity in activities
        ]