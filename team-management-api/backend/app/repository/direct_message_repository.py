from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.direct_message_model import DirectMessage

class DirectMessageRepository:

    async def create_message(
            self,
            db: AsyncSession,
            message: DirectMessage
    ) -> DirectMessage:
        
        db.add(message)
        await db.commit()
        await db.refresh(message)

        result = await db.execute(select(DirectMessage)
                                  .options(selectinload(DirectMessage.sender))
                                  .where(DirectMessage.id == message.id))
        
        return result.scalar_one()
    
    async def get_conversation_messages(
            self,
            db: AsyncSession,
            conversation_id : UUID,
            limit: int = 50
    ) -> list[DirectMessage]:
        
        result = await db.execute(select(DirectMessage)
                                  .options(selectinload(DirectMessage.sender))
                                  .where(DirectMessage.conversation_id == conversation_id)
                                  .order_by(DirectMessage.created_at.desc())
                                  .limit(limit))
        
        return list(result.scalar().all())