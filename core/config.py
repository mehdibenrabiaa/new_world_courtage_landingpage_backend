from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3002"]
    API_KEY: str = "dev-local-key-change-in-prod"
    ENVIRONMENT: str = "production"

    class Config:
        env_file = ".env"

settings = Settings()
