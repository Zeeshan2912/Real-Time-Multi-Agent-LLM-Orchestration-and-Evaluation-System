from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:pass@db:5432/megaai"
    REDIS_URL: str = "redis://cache:6379"
    LOG_LEVEL: str = "INFO"
    MAX_CONTEXT_TOKENS: int = 8000
    LLM_API_KEY: Optional[str] = None
    LLM_BASE_URL: Optional[str] = None
    LLM_MODEL: str = "gpt-4-turbo"
    RANDOM_SEED: int = 42
    LLM_TEMPERATURE: float = 0.0

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()