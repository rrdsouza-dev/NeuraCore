"""Fallback explícito para um backend alternativo."""

from neuracore.backends.base import InferenceBackend


class FallbackBackend(InferenceBackend):
    """Tenta o backend principal e usa o alternativo quando ele falha."""

    def __init__(self, primary: InferenceBackend, fallback: InferenceBackend) -> None:
        self.primary = primary
        self.fallback = fallback

    async def generate(self, prompt: str, *, model: str) -> str:
        try:
            return await self.primary.generate(prompt, model=model)
        except Exception:
            return await self.fallback.generate(prompt, model=model)
