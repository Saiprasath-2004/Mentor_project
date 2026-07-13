from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation_model import Conversation
from app.models.conversation_participant_model import ConversationParticipant
from app.models.user import User

from app.repository.conversation_repository import ConversationRepository
from app.repository.user_repository import UserRepository


class ConversationService: 

    def __init__(self):
        self.conversation_repo = ConversationRepository()
        self.user_repo = UserRepository()
        
    # Return an existing conversation or create a new one
    async def get_or_create_conversation(
        self,
        db:AsyncSession,
        other_user_id:UUID,
        current_user: User
    ) -> Conversation:
        
        if other_user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail= "You cannot start a conversation with yourself"
            )
        
        other_user= await self.user_repo.get_by_id(
            db,
            other_user_id
        )

        if not other_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        conversation = await self.conversation_repo.find_direct_conversation(
            db,
            current_user.id,
            other_user_id
        )

        if conversation:
            return conversation

        conversation = Conversation()

        conversation = await self.conversation_repo.create_conversation(
            db,
            conversation
        )

        await self.conversation_repo.add_participant(
            db,
            ConversationParticipant(
                conversation_id = conversation.id,
                user_id = current_user.id
            )
        )

        await self.conversation_repo.add_participant(
            db,
            ConversationParticipant(
                conversation_id=conversation.id,
                user_id=other_user_id
            )
        )

        conversation: Conversation= await self.conversation_repo.get_conversation_by_id(
            db,
            conversation.id
        )

        return conversation
    
    async def get_conversation(
        self,
        db: AsyncSession,
        conversation_id: UUID,
        current_user: User
    ) -> Conversation:
        """
        Fetch a conversation and ensure the current user
        is one of its participants.
        """

        conversation = await self.conversation_repo.get_conversation_by_id(
            db,
            conversation_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found."
            )

        participant_ids = {
            participant.user_id
            for participant in conversation.participants
        }

        if current_user.id not in participant_ids:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this conversation."
            )

        return conversation
        
            