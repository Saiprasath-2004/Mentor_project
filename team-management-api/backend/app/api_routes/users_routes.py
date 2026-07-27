from fastapi import APIRouter, Depends

from app.dependencies.auth_dependencies import get_current_user
from app.schemas.user_schemas import UserResponse
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Return currently authenticated user's profile
@router.get(
    "/me",
    response_model=UserResponse
)

async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    
    return  current_user
