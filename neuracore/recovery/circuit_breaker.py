"""Circuit breaker assíncrono para proteger backends indisponíveis."""

import time
from collections.abc import Awaitable, Callable
from enum import StrEnum
from typing import TypeVar

T = TypeVar("T")


class CircuitState(StrEnum):
    FECHADO = "fechado"
    ABERTO = "aberto"
    TESTE = "teste"


class CircuitOpenError(RuntimeError):
    """Indica que o circuito está aberto e bloqueou a operação."""


class CircuitBreaker:
    """Bloqueia chamadas após falhas consecutivas e permite um teste posterior."""

    def __init__(self, failure_threshold: int = 3, recovery_timeout_seconds: float = 30.0) -> None:
        if failure_threshold < 1:
            raise ValueError("O limite de falhas deve ser positivo")
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.state = CircuitState.FECHADO
        self._failures = 0
        self._opened_at = 0.0

    async def call(self, operation: Callable[[], Awaitable[T]]) -> T:
        """Executa uma operação ou rejeita enquanto o circuito estiver aberto."""
        if self.state is CircuitState.ABERTO:
            if time.monotonic() - self._opened_at < self.recovery_timeout_seconds:
                raise CircuitOpenError("O circuito está aberto")
            self.state = CircuitState.TESTE
        try:
            result = await operation()
        except Exception:
            self._failures += 1
            if self._failures >= self.failure_threshold:
                self.state = CircuitState.ABERTO
                self._opened_at = time.monotonic()
            raise
        self._failures = 0
        self.state = CircuitState.FECHADO
        return result
