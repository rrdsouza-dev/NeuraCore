from fastapi.testclient import TestClient

from neuracore.api.server import create_app
from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return prompt


def test_metrics_expoe_formato_prometheus() -> None:
    with TestClient(create_app(InferenceEngine(BackendDeTeste()))) as client:
        client.post("/v1/inference", json={"model": "teste", "prompt": "Olá"})
        response = client.get("/metrics")

    assert response.status_code == 200
    assert "neuracore_inference_requests_total" in response.text
    assert "neuracore_inference_duration_seconds" in response.text
