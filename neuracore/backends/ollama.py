"""Integração assíncrona inicial com a API do Ollama."""

from typing import cast

import httpx

from neuracore.backends.base import InferenceBackend
from neuracore.core.config import Settings
from neuracore.recovery.circuit_breaker import CircuitBreaker
from neuracore.recovery.retry import RetryPolicy, execute_with_retry


class OllamaBackend(InferenceBackend):
    """Backend Ollama com geração síncrona e suporte futuro a streaming."""

    def __init__(
        self,
        settings: Settings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings or Settings()
        self._client = client or httpx.AsyncClient(
            base_url=self.settings.ollama_base_url,
            timeout=self.settings.ollama_timeout_seconds,
        )
        self._circuit = CircuitBreaker(
            failure_threshold=self.settings.ollama_circuit_failure_threshold,
            recovery_timeout_seconds=self.settings.ollama_circuit_recovery_seconds,
        )

    async def generate(self, prompt: str, *, model: str) -> str:
        """Gera texto usando o endpoint não-streaming `/api/generate`."""
        payload = {"model": model, "prompt": prompt, "stream": False}

        async def request() -> str:
            response = await self._client.post("/api/generate", json=payload)
            response.raise_for_status()
            return cast(str, response.json()["response"])

        async def resilient_request() -> str:
            def is_transient(error: Exception) -> bool:
                return isinstance(error, httpx.TransportError) or (
                    isinstance(error, httpx.HTTPStatusError) and error.response.status_code >= 500
                )

            return await execute_with_retry(
                request,
                RetryPolicy(
                    attempts=self.settings.ollama_retry_attempts,
                    initial_delay_seconds=self.settings.ollama_retry_delay_seconds,
                    should_retry=is_transient,
                ),
            )

        return await self._circuit.call(resilient_request)

    async def close(self) -> None:
        await self._client.aclose()
