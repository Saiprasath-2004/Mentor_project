from passlib.context import CryptContext

from datetime import datetime,timedelta,timezone
from jose import jwt

from app.core.config import settings

# Password hashing configuration
# bcrypt automatically handles salt generation internally
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Convert plain password into irreversible hashed password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify entered password against stored hashed password
def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

# Create signed JWT access token with user identity and expiration
def create_access_token(user_id: str) -> str:

    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
        
# Decode token and return payload data if signature is valid
def decode_token(token: str):

    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )

    return payload