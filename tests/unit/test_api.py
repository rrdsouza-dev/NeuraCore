from fastapi.testclient import TestClient

from neuracore.api.server import create_app
from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine
from neuracore.resources.monitor import ResourceMonitor, ResourceSnapshot
from neuracore.scheduler.admission import AdmissionPolicy


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return f"resposta para: {prompt}"


class MonitorAlto(ResourceMonitor):
    def snapshot(self) -> ResourceSnapshot:
        return ResourceSnapshot(cpu_percent=99, memory_percent=20, memory_available_bytes=1)


def test_health_retorna_status_ok() -> None:
    with TestClient(create_app(InferenceEngine(BackendDeTeste()))) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_inference_expoe_resposta_normalizada() -> None:
    with TestClient(create_app(InferenceEngine(BackendDeTeste()))) as client:
        response = client.post("/v1/inference", json={"model": "teste", "prompt": "Olá"})

    assert response.status_code == 200
    assert response.json() == {"model": "teste", "text": "resposta para: Olá"}


def test_inference_recusa_recursos_acima_do_limite() -> None:
    from fastapi import FastAPI

    from neuracore.api.routes import create_router

    application = FastAPI()
    application.include_router(
        create_router(
            InferenceEngine(BackendDeTeste()),
            resource_monitor=MonitorAlto(),
            admission_policy=AdmissionPolicy(max_cpu_percent=80),
        )
    )
    with TestClient(application) as client:
        response = client.post("/v1/inference", json={"model": "teste", "prompt": "Olá"})

    assert response.status_code == 503
