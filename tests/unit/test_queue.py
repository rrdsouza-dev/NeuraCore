import pytest

from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest
from neuracore.queue.engine import InferenceQueue


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
