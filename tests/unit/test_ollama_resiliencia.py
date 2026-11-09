import httpx
import pytest

from neuracore.backends.ollama import OllamaBackend
from neuracore.core.config import Settings
from neuracore.recovery.circuit_breaker import CircuitOpenError


@pytest.mark.asyncio
async def test_ollama_abre_circuito_apos_falhas_configuradas() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(503, json={"error": "indisponível"})

    settings = Settings(
        ollama_retry_attempts=1,
        ollama_circuit_failure_threshold=1,
        ollama_circuit_recovery_seconds=60,
    )
    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://ollama") as client:
        backend = OllamaBackend(settings=settings, client=client)
        with pytest.raises(httpx.HTTPStatusError):
            await backend.generate("Oi", model="llama3")
        with pytest.raises(CircuitOpenError):
            await backend.generate("Oi", model="llama3")
