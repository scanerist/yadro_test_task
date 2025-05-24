import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres")
    RANDOMUSER_API_URL: str = "https://randomuser.me/api/"

settings = Settings()

def get_db_url() -> str:
    return settings.DATABASE_URL