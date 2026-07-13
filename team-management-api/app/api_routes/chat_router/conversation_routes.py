from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User

from app.schemas.conversation_schemas import ConversationResponse

from app.services.conversation_service import ConversationService


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)


conversation_service = ConversationService()

@router.post(
    "/{other_user_id}",
    response_model = ConversationResponse
)
async def get_or_create_conversation(
    other_user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    conversation = await conversation_service.get_or_create_conversation(
        db = db,
        other_user_id=other_user_id,
        current_user=current_user
    )

    return ConversationResponse.model_validate(conversation)