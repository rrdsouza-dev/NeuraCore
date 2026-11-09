import pytest

from neuracore.backends.base import InferenceBackend
from neuracore.recovery.circuit_breaker import CircuitBreaker, CircuitOpenError
from neuracore.recovery.fallback import FallbackBackend


class BackendDeTeste(InferenceBackend):
    def __init__(self, resposta: str, falhar: bool = False) -> None:
        self.resposta = resposta
        self.falhar = falhar

    async def generate(self, prompt: str, *, model: str) -> str:
        if self.falhar:
            raise RuntimeError("backend indisponível")
        return self.resposta


@pytest.mark.asyncio
async def test_circuit_breaker_abre_apos_limite_de_falhas() -> None:
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout_seconds=60)

    async def falha() -> str:
        raise RuntimeError("falha")

    for _ in range(2):
        with pytest.raises(RuntimeError):
            await breaker.call(falha)
    with pytest.raises(CircuitOpenError):
        await breaker.call(falha)


@pytest.mark.asyncio
async def test_fallback_usa_backend_alternativo() -> None:
    backend = FallbackBackend(BackendDeTeste("principal", falhar=True), BackendDeTeste("reserva"))

    assert await backend.generate("Olá", model="teste") == "reserva"
