"""Rotas HTTP da API pública inicial."""

from fastapi import APIRouter

from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest, InferenceResponse


def create_router(engine: InferenceEngine) -> APIRouter:
    """Cria as rotas com o motor de inferência injetado."""
    router = APIRouter()

    @router.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.post("/v1/inference", response_model=InferenceResponse)
    async def inference(request: InferenceRequest) -> InferenceResponse:
        return await engine.generate(request)

    return router
