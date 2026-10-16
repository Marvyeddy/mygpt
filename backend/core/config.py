from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., alias="DATABASE_URL")
    TEST_DB_URL: str = Field(..., alias="TEST_DB_URL")

    @computed_field
    def LANGGRAPH_DB_URI(self) -> str:  # 💡 Removed @property and added -> str
        return self.DATABASE_URL.replace("+psycopg", "")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore"
    )


config = Settings()
