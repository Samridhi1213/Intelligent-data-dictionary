import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database Settings
    DB_TYPE: str = "postgresql"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123456"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_NAME: str = "olist_db"

    # Gemini Settings
    GEMINI_API_KEY: str = ""

    # Export Settings
    EXPORT_PATH: str = "./exports"

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def DATABASE_URL(self) -> str:
        return f"{self.DB_TYPE}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
# print(f"DEBUG: API Key identified: {bool(settings.OPENAI_API_KEY)}") # Helper to check in logs
