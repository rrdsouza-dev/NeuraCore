from fastapi.testclient import TestClient

from neuracore.api.server import create_app
from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return f"resposta para: {prompt}"


def test_health retorna_status_ok() -> None:
    client = TestClient(create_app(InferenceEngine(BackendDeTeste())))
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_inference_expoe_resposta_normalizada() -> None:
    client = TestClient(create_app(InferenceEngine(BackendDeTeste())))
    response = client.post("/v1/inference", json={"model": "teste", "prompt": "Olá"})

    assert response.status_code == 200
    assert response.json() == {"model": "teste", "text": "resposta para: Olá"}
