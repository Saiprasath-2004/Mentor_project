from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.direct_message_model import DirectMessage

from app.repository.direct_message_repository import DirectMessageRepository

from app.services.conversation_service import ConversationService

from app.schemas.direct_message_schemas import (
    DirectMessageCreate,
    DirectMessageResponse
)

class DirectMessageService:

    def __init__(self):
        self.message_repo = DirectMessageRepository()
        self.conversation_service = ConversationService()

    def built_message_response(self,message: DirectMessage) -> DirectMessageResponse:
        return DirectMessageResponse(
            id = message.id,
            conversation_id = message.conversation_id,
            sender_id=message.sender_id,
            sender_name=message.sender.username,
            message=message.message,
            created_at=message.created_at
        )
    
    async def send_message(
        self,
        db: AsyncSession,
        conversation_id: UUID,
        message_data: DirectMessageCreate,
        current_user: User
    ) -> DirectMessageResponse:

        conversation = await self.conversation_service.get_conversation(
            db=db,
            conversation_id=conversation_id,
            current_user=current_user
        )

        message = DirectMessage(
            conversation_id=conversation.id,
            sender_id=current_user.id,
            message=message_data.message
        )

        message = await self.message_repo.create_message(
            db,
            message
        )

        return self.built_message_response(message)

    async def get_history(
            self,
            db: AsyncSession,
            conversation_id : UUID,
            current_user: User
    ) -> list[DirectMessageResponse]:
        
        #Validate access to conversation
        conversation = await self.conversation_service.get_conversation(
            db = db,
            conversation_id=conversation_id,
            current_user=current_user
        )

        #Load latest messages
        messages = await self.message_repo.get_conversation_messages(
            db,
            conversation.id
        )

        return [
            self.built_message_response(message)
            for message in reversed(messages)
        ]