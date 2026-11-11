"""Modelos de entrada e saída da inferência."""

from pydantic import BaseModel, Field

from neuracore.queue.policies import Priority


class InferenceRequest(BaseModel):
    """Solicitação mínima para geração de texto."""

    prompt: str = Field(min_length=1)
    model: str = Field(min_length=1)
    priority: Priority = Priority.NORMAL
    session_id: str | None = None


class InferenceResponse(BaseModel):
    """Resposta normalizada de um backend."""

    model: str
    text: str
