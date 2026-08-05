from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings."""

    def __init__(self) -> None:

        #db
        self.database_url: str = os.getenv(
            "DATABASE_URL",
            "postgresql://datatalk_user:datatalk_password@localhost:5432/northwind",
        )

        # Gemini Config
        self.gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
        self.gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.gemini_temperature: float = float(os.getenv("GEMINI_TEMPERATURE", "0.1"))

        # LLM Provider
        self.llm_provider: str = os.getenv("LLM_PROVIDER", "gemini")

        # Application
        self.app_env: str = os.getenv("APP_ENV", "development")
        self.debug: bool = self._parse_bool(os.getenv("DEBUG", "false"))

        # Security
        self.query_timeout_seconds: int = int(os.getenv("QUERY_TIMEOUT", "30"))
        self.max_rows: int = int(os.getenv("MAX_ROWS", "1000"))
        self.max_retries: int = int(os.getenv("MAX_RETRIES", "3"))

    @staticmethod
    def _parse_bool(value: str) -> bool:
        return value.strip().lower() in {"1", "true", "yes", "on"}


settings = Settings()
