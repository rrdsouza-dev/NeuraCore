from fastapi.testclient import TestClient

from neuracore.api.server import create_app
from neuracore.backends.base import InferenceBackend
from neuracore.core.config import Settings
from neuracore.inference.engine import InferenceEngine


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return prompt


def test_api_exige_chave_quando_configurada() -> None:
    app = create_app(
        InferenceEngine(BackendDeTeste()),
        settings=Settings(api_key="segredo"),
    )
    with TestClient(app) as client:
        sem_chave = client.get("/health")
        com_chave = client.get("/health", headers={"X-API-Key": "segredo"})

    assert sem_chave.status_code == 401
    assert com_chave.status_code == 200
