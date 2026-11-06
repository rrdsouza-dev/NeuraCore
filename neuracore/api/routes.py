"""Rotas HTTP da API pública inicial."""

from fastapi import APIRouter
from fastapi.responses import Response

from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest, InferenceResponse
from neuracore.monitoring.metrics import inference_requests, render_metrics


def create_router(engine: InferenceEngine) -> APIRouter:
    """Cria as rotas com o motor de inferência injetado."""
    router = APIRouter()

    @router.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(content=render_metrics(), media_type="text/plain; version=0.0.4")

    @router.post("/v1/inference", response_model=InferenceResponse)
    async def inference(request: InferenceRequest) -> InferenceResponse:
        inference_requests.inc()
        return await engine.generate(request)

    return router
