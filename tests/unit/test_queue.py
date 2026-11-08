import asyncio

import pytest

from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest
from neuracore.queue.engine import InferenceQueue, QueueFullError


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return f"{model}:{prompt}"


@pytest.mark.asyncio
async def test_fila_processa_solicitacao() -> None:
    queue = InferenceQueue(InferenceEngine(BackendDeTeste()))
    await queue.start()

    response = await queue.submit(InferenceRequest(model="teste", prompt="Olá"))
    await queue.stop()

    assert response.text == "teste:Olá"


@pytest.mark.asyncio
async def test_fila_exige_inicio_antes_do_envio() -> None:
    queue = InferenceQueue(InferenceEngine(BackendDeTeste()))

    with pytest.raises(RuntimeError, match="não foi iniciada"):
        await queue.submit(InferenceRequest(model="teste", prompt="Olá"))


@pytest.mark.asyncio
async def test_fila_rejeita_excesso_de_solicitacoes() -> None:
    queue = InferenceQueue(InferenceEngine(BackendDeTeste()), max_size=1)
    await queue.start()
    queue._jobs.put_nowait(
        (
            InferenceRequest(model="teste", prompt="ocupada"),
            asyncio.get_running_loop().create_future(),
        )
    )

    with pytest.raises(QueueFullError, match="fila de inferência está cheia"):
        await queue.submit(InferenceRequest(model="teste", prompt="excesso"))

    await queue.stop()
