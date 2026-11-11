"""Factory da aplicação FastAPI."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from neuracore.api.routes import create_router
from neuracore.core.config import Settings
from neuracore.inference.engine import InferenceEngine, create_default_engine
from neuracore.inference.sessions import SQLiteSessionStore, SessionStore
from neuracore.queue.engine import InferenceQueue


def create_app(
    engine: InferenceEngine | None = None,
    settings: Settings | None = None,
) -> FastAPI:
    """Cria a aplicação com dependências explícitas e configuração padrão."""
    runtime_settings = settings or Settings()
    runtime_engine = engine or create_default_engine(runtime_settings)
    inference_queue = InferenceQueue(
        runtime_engine,
        max_size=runtime_settings.inference_queue_max_size,
    )
    session_store: SessionStore = (
        SQLiteSessionStore(runtime_settings.session_database_path)
        if runtime_settings.session_database_path
        else SessionStore()
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        await inference_queue.start()
        try:
            yield
        finally:
            await inference_queue.stop()

    application = FastAPI(title="NeuraCore", version="0.1.0", lifespan=lifespan)
    application.include_router(
        create_router(
            runtime_engine,
            inference_queue=inference_queue,
            session_store=session_store,
            api_key=runtime_settings.api_key,
        )
    )
    return application


app = create_app()
