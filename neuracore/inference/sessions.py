"""Sessões de conversa mantidas em memória durante o processo."""

from datetime import UTC, datetime
from uuid import uuid4

from pydantic import BaseModel, Field


class SessionMessage(BaseModel):
    """Mensagem registrada em uma sessão."""

    role: str
    content: str


class Session(BaseModel):
    """Estado de uma conversa local."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    messages: list[SessionMessage] = Field(default_factory=list)


class SessionStore:
    """Armazena sessões em memória; persistência será adicionada depois."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def create(self) -> Session:
        """Cria e registra uma sessão vazia."""
        session = Session()
        self._sessions[session.id] = session
        return session

    def get(self, session_id: str) -> Session:
        """Retorna uma sessão existente."""
        try:
            return self._sessions[session_id]
        except KeyError as error:
            raise KeyError(f"Sessão não encontrada: {session_id}") from error

    def append(self, session_id: str, message: SessionMessage) -> Session:
        """Adiciona uma mensagem e retorna o estado atualizado."""
        session = self.get(session_id)
        session.messages.append(message)
        return session
