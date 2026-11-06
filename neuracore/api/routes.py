"""Rotas HTTP da API pública inicial."""

from fastapi import APIRouter
from fastapi.responses import Response

from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest, InferenceResponse
from neuracore.monitoring.metrics import inference_requests, render_metrics
from neuracore.resources.monitor import ResourceMonitor, ResourceSnapshot


def create_router(
    engine: InferenceEngine,
    resource_monitor: ResourceMonitor | None = None,
) -> APIRouter:
    """Cria as rotas com o motor de inferência injetado."""
    router = APIRouter()
    monitor = resource_monitor or ResourceMonitor()

    @router.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/health/resources", response_model=ResourceSnapshot)
    async def health_resources() -> ResourceSnapshot:
        return monitor.snapshot()

    @router.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(content=render_metrics(), media_type="text/plain; version=0.0.4")

    @router.post("/v1/inference", response_model=InferenceResponse)
    async def inference(request: InferenceRequest) -> InferenceResponse:
        inference_requests.inc()
        return await engine.generate(request)

    return router
