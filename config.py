import os
from dataclasses import dataclass

from dotenv import load_dotenv

from database.safety import redact_sensitive_data

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_name: str = "SQLPilot"
    app_environment: str = os.getenv("APP_ENV", "development")
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")
    default_database: str = os.getenv("DEFAULT_DATABASE", "postgres")
    default_model: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    streamlit_port: int = int(os.getenv("STREAMLIT_PORT", "8501"))

    @property
    def redacted_database_url(self) -> str:
        return redact_sensitive_data(self.database_url)

    @property
    def redacted_openai_api_key(self) -> str:
        return "***" if self.openai_api_key else ""


settings = Settings()
