from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import UserCreate, UserResponse
from app.schemas.auth_schemas import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.core.database import get_db


router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_service = AuthService()


# Register new user endpoint
@router.post( "/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):

        return await auth_service.register(
            db,
            user_data
        )    


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db:AsyncSession = Depends(get_db)):
        return await auth_service.login(
                db,
                login_data
        )

