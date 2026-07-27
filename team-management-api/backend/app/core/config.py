from pydantic_settings import BaseSettings, SettingsConfigDict


# Centralized application configuration loaded from .env
# Keeps secrets/config outside source code (single source of truth)
class Settings(BaseSettings):
    DATABASE_URL: str               # PostgreSQL connection string
    ALEMBIC_DATABASE_URL: str       # postgres connection for sync ALembic 
    SECRET_KEY: str                 # Used for signing JWT tokens
    ALGORITHM: str                  # JWT signing algorithm (ex: HS256)
    ACCESS_TOKEN_EXPIRE_MINUTES: int # Access token expiration time
    FRONTEND_URL: str
    
    model_config = SettingsConfigDict(
        env_file=".env"
    )


# Global settings object accessible across entire application
settings = Settings()