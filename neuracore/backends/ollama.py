"""Ollama backend placeholder and integration boundary."""

from neuracore.backends.base import InferenceBackend
from neuracore.core.config import Settings


class OllamaBackend(InferenceBackend):
    """First backend boundary; transport and streaming are intentionally pending."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or Settings()

    async def generate(self, prompt: str, *, model: str) -> str:
        raise NotImplementedError("Ollama generation is not implemented yet")
