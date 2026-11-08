"""Integração assíncrona inicial com a API do Ollama."""

from typing import cast

import httpx

from neuracore.backends.base import InferenceBackend
from neuracore.core.config import Settings
from neuracore.recovery.retry import RetryPolicy, execute_with_retry


class OllamaBackend(InferenceBackend):
    """Backend Ollama com geração síncrona e suporte futuro a streaming."""

    def __init__(
        self,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings or Settings()
        self._client = client

    async def generate(self, prompt: str, *, model: str) -> str:
        """Gera texto usando o endpoint não-streaming `/api/generate`."""
        payload = {"model": model, "prompt": prompt, "stream": False}

        async def request() -> str:
            if self._client is None:
                async with httpx.AsyncClient(
                    base_url=self.settings.ollama_base_url,
                    timeout=self.settings.ollama_timeout_seconds,
                ) as client:
                    response = await client.post("/api/generate", json=payload)
            else:
                response = await self._client.post("/api/generate", json=payload)
            response.raise_for_status()
            return cast(str, response.json()["response"])

        return await execute_with_retry(
            request,
            RetryPolicy(
                attempts=self.settings.ollama_retry_attempts,
                initial_delay_seconds=self.settings.ollama_retry_delay_seconds,
            ),
        )
