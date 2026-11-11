"""Sessões de conversa mantidas em memória durante o processo."""

from datetime import UTC, datetime
import json
import sqlite3
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


class SQLiteSessionStore(SessionStore):
    """Armazena sessões em SQLite para sobreviver ao reinício do processo."""

    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self._connection = sqlite3.connect(database_path, check_same_thread=False)
        self._connection.execute(
            "CREATE TABLE IF NOT EXISTS sessions "
            "(id TEXT PRIMARY KEY, created_at TEXT NOT NULL, messages TEXT NOT NULL)"
        )
        self._connection.commit()

    def create(self) -> Session:
        session = Session()
        self._connection.execute(
            "INSERT INTO sessions (id, created_at, messages) VALUES (?, ?, ?)",
            (session.id, session.created_at.isoformat(), "[]"),
        )
        self._connection.commit()
        return session

    def get(self, session_id: str) -> Session:
        row = self._connection.execute(
            "SELECT id, created_at, messages FROM sessions WHERE id = ?", (session_id,)
        ).fetchone()
        if row is None:
            raise KeyError(f"Sessão não encontrada: {session_id}")
        return Session(
            id=row[0],
            created_at=datetime.fromisoformat(row[1]),
            messages=[SessionMessage.model_validate(item) for item in json.loads(row[2])],
        )

    def append(self, session_id: str, message: SessionMessage) -> Session:
        session = self.get(session_id)
        session.messages.append(message)
        messages_json = json.dumps([item.model_dump() for item in session.messages])
        self._connection.execute(
            "UPDATE sessions SET messages = ? WHERE id = ?",
            (messages_json, session_id),
        )
        self._connection.commit()
        return session
