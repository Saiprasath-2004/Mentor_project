from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from  app.models.user import User

class UserRepository:

    # Find user by email during login/register flow
    async def get_by_email( self,  db: AsyncSession, email:str):
        query = select(User).where(User.email==email)

        result = await db.execute(query)

        return result.scalar_one_or_none()
    

    # Create new user record
    async def create_user( self, db: AsyncSession, user_data: dict):
        user = User(**user_data)
        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user
    
    # Find user using unique user ID from JWT token
    async def get_by_id(self,db: AsyncSession,user_id: str):
        query = select(User).where(User.id == user_id)
        
        result = await db.execute(query)
        return result.scalar_one_or_none()