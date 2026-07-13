from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chat_message_model import ChatMessage

class ChatRepository:

    async def create_message(
            self,
            db: AsyncSession,
            message: ChatMessage
    ) -> ChatMessage:
        
        db.add(message)

        await db.commit()

        await db.refresh(message)

        result = await db.execute(
            select(ChatMessage)
            .options(selectinload(ChatMessage.sender))
            .where(ChatMessage.id == message.id)
        )

        return result.scalar_one()
    
    async def get_team_messages(
            self,
            db:AsyncSession,
            team_id: UUID,
            limit: int = 50
    ) -> list[ChatMessage]:
        
        #Return the latest messages for a team.

        query = (select(ChatMessage)
                 .options(selectinload(ChatMessage.sender))
                 .where(ChatMessage.team_id == team_id)
                 .order_by(ChatMessage.created_at.desc())
                 .limit(limit))
        
        result = await db.execute(query)

        return list(result.scalars().all())