from app.schemas.user import UserCreate, UserResponse
from app.repository.user_repository import UserRepository
from app.core.security import hash_password


class AuthService:

    def __init__(self):
        self.user_repo = UserRepository()


    # Register new user after validating business rules
    async def register(
        self,
        db,
        user_data: UserCreate
    ):

        # Check if email already exists
        existing_user = await self.user_repo.get_by_email(
            db,
            user_data.email
        )

        if existing_user:
            raise ValueError("User already exists")


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