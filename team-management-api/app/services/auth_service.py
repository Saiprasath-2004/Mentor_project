from fastapi import HTTPException

from app.schemas.user_schemas import UserCreate, UserResponse
from app.schemas.auth_schemas import LoginRequest, TokenResponse
from app.repository.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()

    # Register new user after validating business rules
    async def register(self, db, user_data: UserCreate):

       # Prevent duplicate account creation using same email
        existing_user = await self.user_repo.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="User already exists"
            )
         
        # Convert schema to dictionary
        user_dict = user_data.model_dump()


        # Hash plain password before storing
        hashed_password = hash_password(
            user_dict.pop("password")
        ) 


        # Prepare final DB payload
        user_dict["hashed_password"] = hashed_password


        # Save user in database
        user = await self.user_repo.create_user(
            db,
            user_dict
        )


        # Return safe response schema
        return UserResponse.model_validate(user)
    
    async def login(self, db, login_data: LoginRequest):

        #check whether account exists
        user = await self.user_repo.get_by_email(
            db,
            login_data.email
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        # Verify entered password against stored hash
        is_valid = verify_password(
            login_data.password,
            user.hashed_password
        )

        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )
        
        #Generate signed JWT token for authenticated user
        access_token = create_access_token(
            str(user.id)
        )

        return TokenResponse(
            access_token=access_token
        )