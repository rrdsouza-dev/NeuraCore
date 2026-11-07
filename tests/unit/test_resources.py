from fastapi.testclient import TestClient

from neuracore.api.server import create_app
from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine
from neuracore.resources.monitor import ResourceMonitor


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return prompt


def test_monitor_coleta_recursos_basicos() -> None:
    snapshot = ResourceMonitor().snapshot()

    assert snapshot.cpu_percent >= 0
    assert snapshot.memory_percent >= 0
    assert snapshot.memory_available_bytes > 0


def test_api_expoe_recursos_do_sistema() -> None:
    with TestClient(create_app(InferenceEngine(BackendDeTeste()))) as client:
        response = client.get("/health/resources")

    assert response.status_code == 200
    assert set(response.json()) == {
        "cpu_percent",
        "memory_percent",
        "memory_available_bytes",
    }
