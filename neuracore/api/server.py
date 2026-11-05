"""Factory da aplicação FastAPI."""

from fastapi import FastAPI

from neuracore.api.routes import create_router
from neuracore.inference.engine import InferenceEngine, create_default_engine


def create_app(engine: InferenceEngine | None = None) -> FastAPI:
    """Cria a aplicação com dependências explícitas e configuração padrão."""
    application = FastAPI(title="NeuraCore", version="0.1.0")
    application.include_router(create_router(engine or create_default_engine()))
    return application


app = create_app()
