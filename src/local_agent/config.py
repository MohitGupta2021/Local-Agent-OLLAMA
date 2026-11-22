from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    ollama_base_url: str = "http://localhost:11434/v1"
    agent_model: str = "qwen2.5:3b"
    agent_timeout: float = Field(default=60.0, gt=0)
    notes_file: Path = Path("data/notes.jsonl")
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings()
