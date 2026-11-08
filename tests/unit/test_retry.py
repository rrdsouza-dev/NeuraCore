import pytest

from neuracore.recovery.retry import RetryPolicy, execute_with_retry


@pytest.mark.asyncio
async def test_retry_tenta_novamente_ate_sucesso() -> None:
    tentativas = 0

    async def operação() -> str:
        nonlocal tentativas
        tentativas += 1
        if tentativas < 2:
            raise RuntimeError("falha transitória")
        return "ok"

    resultado = await execute_with_retry(operação, RetryPolicy(attempts=2, initial_delay_seconds=0))

    assert resultado == "ok"
    assert tentativas == 2


@pytest.mark.asyncio
async def test_retry_preserva_ultimo_erro() -> None:
    async def operação() -> str:
        raise RuntimeError("falha final")

    with pytest.raises(RuntimeError, match="falha final"):
        await execute_with_retry(operação, RetryPolicy(attempts=2, initial_delay_seconds=0))
