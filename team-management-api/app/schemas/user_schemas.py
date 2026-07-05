from uuid import   UUID

from pydantic import BaseModel, EmailStr, Field

# Shared user fields reused across schemas
class UserBase(BaseModel):
    email:EmailStr
    username: str = Field(min_length=3,max_length=30)

# Used when creating/registering new user
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# Sent back in API responses
# Only expose safe fields
class UserResponse(UserBase):
    id: UUID
    model_config={
        "from_attributes":True
    }