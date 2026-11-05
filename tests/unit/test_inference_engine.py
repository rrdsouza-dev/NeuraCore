from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return f"{model}: {prompt}"


async def test_engine_normaliza_resposta_do_backend() -> None:
    engine = InferenceEngine(BackendDeTeste())
    response = await engine.generate(InferenceRequest(prompt="Oi", model="teste"))

    assert response.model == "teste"
    assert response.text == "teste: Oi"
