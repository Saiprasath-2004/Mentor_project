from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.conversation_model import Conversation
from app.models.conversation_participant_model import ConversationParticipant

class ConversationRepository:

    async def create_conversation(
        self,
        db: AsyncSession,
        conversation : Conversation
    ) -> Conversation:
        
        db.add(conversation)

        await db.commit()

        await db.refresh(conversation)

        return conversation
    
    async def add_participant(
        self,
        db: AsyncSession,
        participant: ConversationParticipant
    ) -> ConversationParticipant:
        
        db.add(participant)

        await db.commit()

        await db.refresh(participant)

        return participant
    

    async def get_conversation_by_id(
        self,
        db: AsyncSession,
        conversation_id: UUID
    ) -> Conversation | None:
        
        result  = await db.execute(
            select(Conversation)
            .options(selectinload(Conversation.participants))
            .where(Conversation.id == conversation_id)
        )

        return result.scalar_one_or_none()

    async def get_user_conversations(
        self,
        db: AsyncSession,
        user_id: UUID    
    ) -> list [Conversation]:
        
        #Return every converation the given user belongs to

        result = await db.execute(
            select(Conversation)
            .join(ConversationParticipant)
            .options(
                selectinload(Conversation.participants)
            )
            .where(ConversationParticipant.user_id == user_id)
        )

        return list(result.scalars().all())


    async def find_direct_conversation(
            self,
            db: AsyncSession,
            user1_id: UUID,
            user2_id: UUID,
    ) -> Conversation | None:
        
        ## Return the existing direct conversation between two users if exisits

        conversations = await self.get_user_conversations(
            db,
            user1_id
        )

        for conversation in conversations:

            participant_ids = {
                #Example of what happens
                # {
                #    sai_id, => main user
                #    rahul_id => => chatting user with  main user
                #  }
                

                participant.user_id
                for participant in conversation.participants
            }
            # we use set here instead of the list because in the user1 , user2 == user2, user 1 from the table 
            if participant_ids == {user1_id,user2_id}:
                return conversation
            
        return None