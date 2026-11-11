"""Factory da aplicação FastAPI."""

from collections.abc import AsyncIterator, Awaitable, Callable
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request, Response

from neuracore.api.routes import create_router
from neuracore.core.config import Settings
from neuracore.inference.engine import InferenceEngine, create_default_engine
from neuracore.inference.sessions import SessionStore, SQLiteSessionStore
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
        workers=runtime_settings.inference_queue_workers,
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

    @application.middleware("http")
    async def request_id_middleware(
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response

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
