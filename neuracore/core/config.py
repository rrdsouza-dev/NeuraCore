"""Central application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables and .env."""

    app_name: str = "NeuraCore"
    inference_backend: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    ollama_timeout_seconds: float = 60.0
    inference_queue_max_size: int = 100
    ollama_retry_attempts: int = 2
    ollama_retry_delay_seconds: float = 0.1
    ollama_circuit_failure_threshold: int = 3
    ollama_circuit_recovery_seconds: float = 30.0
    fallback_base_url: str | None = None
    fallback_api_key: str | None = None
    api_key: str | None = None
    model_config = SettingsConfigDict(env_prefix="NEURACORE_", env_file=".env", extra="ignore")
