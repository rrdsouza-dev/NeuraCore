"""Orquestração mínima do fluxo de inferência."""

from neuracore.backends.base import InferenceBackend
from neuracore.inference.requests import InferenceRequest, InferenceResponse


class InferenceEngine:
    """Executa uma solicitação usando um backend injetado."""

    def __init__(self, backend: InferenceBackend) -> None:
        self.backend = backend

    async def generate(self, request: InferenceRequest) -> InferenceResponse:
        """Envia a solicitação ao backend e normaliza o resultado."""
        text = await self.backend.generate(request.prompt, model=request.model)
        return InferenceResponse(model=request.model, text=text)
