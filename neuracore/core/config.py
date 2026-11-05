"""Central application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables and .env."""

    app_name: str = "NeuraCore"
    inference_backend: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_timeout_seconds: float = 60.0
    model_config = SettingsConfigDict(env_prefix="NEURACORE_", env_file=".env", extra="ignore")
