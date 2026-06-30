from pydantic import BaseModel, EmailStr, Field

# Login request schema
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


# JWT token response returned after successful login
class TokenRequest(BaseModel):
    access_token: str
    token_type: str = "bearer" 