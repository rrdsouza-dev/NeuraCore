"""Execução com tentativas limitadas e atraso progressivo."""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class RetryPolicy:
    """Parâmetros de retry para uma operação assíncrona."""

    attempts: int = 2
    initial_delay_seconds: float = 0.1
    should_retry: Callable[[Exception], bool] | None = None


async def execute_with_retry(operation: Callable[[], Awaitable[T]], policy: RetryPolicy) -> T:
    """Executa a operação até obter sucesso ou esgotar as tentativas."""
    if policy.attempts < 1:
        raise ValueError("O número de tentativas deve ser positivo")
    last_error: Exception | None = None
    for attempt in range(policy.attempts):
        try:
            return await operation()
        except Exception as error:
            last_error = error
            if policy.should_retry is not None and not policy.should_retry(error):
                raise
            if attempt + 1 < policy.attempts:
                await asyncio.sleep(policy.initial_delay_seconds * (2**attempt))
    assert last_error is not None
    raise last_error
