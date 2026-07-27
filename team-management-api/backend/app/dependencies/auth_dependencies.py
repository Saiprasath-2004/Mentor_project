from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import decode_token
from app.repository.user_repository import UserRepository


# Extract Bearer token from Authorization header automatically
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

user_repo = UserRepository()

#Validate JWT and return currently logged in User 
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        # Decode JWT and extract payload
        payload = decode_token(token)

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
    

        # Find actual user in database
        user = await user_repo.get_by_id(
            db,
            user_id
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )
        return user
    
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )