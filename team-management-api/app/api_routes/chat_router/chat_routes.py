from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User
from app.schemas.chat_schemas import ChatMessageResponse
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/teams",
    tags=["Chat"]
)

chat_service = ChatService()

@router.get(
    "/{team_id}/messages",
    response_model=list[ChatMessageResponse]
)
async def get_chat_history(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ##Return the latest chat history for a team

    return await chat_service.get_history(
        db = db,
        team_id=team_id,
        current_user=current_user
    )