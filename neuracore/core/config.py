"""Central application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables and .env."""

    app_name: str = "NeuraCore"
    ollama_base_url: str = "http://localhost:11434"
    model_config = SettingsConfigDict(env_prefix="NEURACORE_", env_file=".env", extra="ignore")
