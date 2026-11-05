"""Orquestração mínima do fluxo de inferência."""

from neuracore.backends.base import InferenceBackend
from neuracore.backends.ollama import OllamaBackend
from neuracore.core.config import Settings
from neuracore.inference.requests import InferenceRequest, InferenceResponse


class InferenceEngine:
    """Executa uma solicitação usando um backend injetado."""

    def __init__(self, backend: InferenceBackend) -> None:
        self.backend = backend

    async def generate(self, request: InferenceRequest) -> InferenceResponse:
        """Envia a solicitação ao backend e normaliza o resultado."""
        text = await self.backend.generate(request.prompt, model=request.model)
        return InferenceResponse(model=request.model, text=text)


def create_default_engine(settings: Settings | None = None) -> InferenceEngine:
    """Cria o motor com o backend inicial definido nas configurações."""
    runtime_settings = settings or Settings()
    if runtime_settings.inference_backend != "ollama":
        raise ValueError(f"Backend padrão não suportado: {runtime_settings.inference_backend}")
    return InferenceEngine(OllamaBackend(runtime_settings))
