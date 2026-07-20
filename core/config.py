from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3002"]
    API_KEY: str = "dev-local-key-change-in-prod"
    ENVIRONMENT: str = "production"

    # Meta WhatsApp Cloud API notification — leave unset to disable.
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_ACCESS_TOKEN: str = ""
    WHATSAPP_NOTIFY_TO: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
