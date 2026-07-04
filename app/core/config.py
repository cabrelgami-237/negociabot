from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "negociabot-secret-key-cameroun-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "postgresql://postgres:admin1234@localhost:5432/negociabot_db"

    class Config:
        env_file = ".env"
        env_file = ".env"
        extra = "ignore"


settings = Settings()