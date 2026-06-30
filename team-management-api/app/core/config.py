from pydantic_settings import BaseSettings


# Centralized application configuration loaded from .env
# Keeps secrets/config outside source code (single source of truth)
class Settings(BaseSettings):
    DATABASE_URL: str               # PostgreSQL connection string
    SECRET_KEY: str                # Used for signing JWT tokens
    ALGORITHM: str                # JWT signing algorithm (ex: HS256)
    ACCESS_TOKEN_EXPIRE_MINUTES: int   # Access token expiration time


# Global settings object accessible across entire application
settings = Settings()