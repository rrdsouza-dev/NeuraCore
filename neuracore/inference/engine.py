"""Orquestração mínima do fluxo de inferência."""

from neuracore.backends.base import InferenceBackend
from neuracore.backends.ollama import OllamaBackend
from neuracore.backends.openai_compatible import OpenAICompatibleBackend
from neuracore.core.config import Settings
from neuracore.inference.requests import InferenceRequest, InferenceResponse
from neuracore.monitoring.tracing import tracer
from neuracore.recovery.fallback import FallbackBackend


class InferenceEngine:
    """Executa uma solicitação usando um backend injetado."""

    def __init__(self, backend: InferenceBackend) -> None:
        self.backend = backend

    async def generate(self, request: InferenceRequest) -> InferenceResponse:
        """Envia a solicitação ao backend e normaliza o resultado."""
        with tracer.start_as_current_span("neuracore.inference") as span:
            span.set_attribute("neuracore.model", request.model)
            text = await self.backend.generate(request.prompt, model=request.model)
            span.set_attribute("neuracore.response_length", len(text))
            return InferenceResponse(model=request.model, text=text)


def create_default_engine(settings: Settings | None = None) -> InferenceEngine:
    """Cria o motor com o backend inicial definido nas configurações."""
    runtime_settings = settings or Settings()
    if runtime_settings.inference_backend != "ollama":
        raise ValueError(f"Backend padrão não suportado: {runtime_settings.inference_backend}")
    primary = OllamaBackend(runtime_settings)
    if runtime_settings.fallback_base_url:
        fallback = OpenAICompatibleBackend(
            runtime_settings.fallback_base_url,
            api_key=runtime_settings.fallback_api_key,
        )
        return InferenceEngine(FallbackBackend(primary, fallback))
    return InferenceEngine(primary)
