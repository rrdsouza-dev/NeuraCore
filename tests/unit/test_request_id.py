from fastapi.testclient import TestClient

from neuracore.api.server import create_app
from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return prompt


def test_api_preserva_request_id_informado() -> None:
    with TestClient(create_app(InferenceEngine(BackendDeTeste()))) as client:
        response = client.get("/health", headers={"X-Request-ID": "teste-123"})

    assert response.headers["X-Request-ID"] == "teste-123"
