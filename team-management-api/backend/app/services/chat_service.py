from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_message_model import ChatMessage
from app.models.user import User
from app.repository.chat_repository import ChatRepository
from app.repository.team_repository import TeamRepository
from app.repository.team_member_repository import TeamMemberRepository
from app.schemas.chat_schemas import (
    ChatMessageCreate,
    ChatMessageResponse
)


class ChatService:

    def __init__(self):
        self.chat_repo = ChatRepository()
        self.team_repo = TeamRepository()
        self.member_repo = TeamMemberRepository()

    
    def build_chat_response(
            self,
            chat:ChatMessage
    ) -> ChatMessageResponse:
        
        return ChatMessageResponse(
            id=chat.id,
            team_id=chat.team_id,
            sender_id=chat.sender_id,
            sender_name=chat.sender.username,
            message=chat.message,
            created_at=chat.created_at
        )

    async def validate_team_access(
        self,
        db: AsyncSession,
        team_id: UUID,
        current_user: User,
    ):
        ### Ensure the team exists and the current user is allowed to access its chat.
        ### Team owners always have access. Team members also have access.

        team = await self.team_repo.get_team_by_id(
            db,
            team_id
        )

        if not team:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Team not found."
            )

        # Owner always has access
        if team.owner_id == current_user.id:
            return team

        # Otherwise user must belong to the team
        member = await self.member_repo.get_member(
            db,
            team_id,
            current_user.id
        )

        if not member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not a member of this team."
            )

        return team

    async def create_message(
        self,
        db: AsyncSession,
        team_id: UUID,
        message_data: ChatMessageCreate,
        current_user: User
    ) -> ChatMessageResponse:

        await self.validate_team_access(
            db,
            team_id,
            current_user
        )

        chat = ChatMessage(
            team_id=team_id,
            sender_id=current_user.id,
            message=message_data.message
        )

        chat = await self.chat_repo.create_message(
            db,
            chat
        )

        return self.build_chat_response(chat)

    async def get_history(
        self,
        db: AsyncSession,
        team_id: UUID,
        current_user: User
    ) -> list[ChatMessageResponse]:

        await self.validate_team_access(
            db,
            team_id,
            current_user
        )

        messages = await self.chat_repo.get_team_messages(
            db,
            team_id
        )

        return [
            self.build_chat_response(message)
            for message in reversed(messages)
        ]