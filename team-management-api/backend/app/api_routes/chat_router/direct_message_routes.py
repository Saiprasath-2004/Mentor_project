from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.dependencies.auth_dependencies import get_current_user

from app.models.user import User

from app.schemas.direct_message_schemas import (
    DirectMessageCreate,
    DirectMessageResponse
)

from app.services.direct_message_service import DirectMessageService

router = APIRouter(
    prefix="/conversations",
    tags=["Direct Messages"]
)

message_service = DirectMessageService()


@router.post(
    "/{conversation_id}/messages",
    response_model=DirectMessageResponse,
    status_code=status.HTTP_201_CREATED
)
async def send_message(
    conversation_id: UUID,
    message_data: DirectMessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await message_service.send_message(
        db=db,
        conversation_id=conversation_id,
        message_data=message_data,
        current_user=current_user
    )


@router.get(
    "/{conversation_id}/messages",
    response_model=list[DirectMessageResponse]
)
async def get_history(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await message_service.get_history(
        db=db,
        conversation_id=conversation_id,
        current_user=current_user
    )