from neuracore.backends.ollama import OllamaBackend
from neuracore.core.config import Settings
from neuracore.inference.engine import create_default_engine
from neuracore.recovery.fallback import FallbackBackend


def test_fabrica_usa_ollama_por_padrao() -> None:
    engine = create_default_engine(Settings())

    assert isinstance(engine.backend, OllamaBackend)


def test_fabrica_configura_fallback_compatível() -> None:
    settings = Settings(fallback_base_url="http://servidor", fallback_api_key="chave")
    engine = create_default_engine(settings)

    assert isinstance(engine.backend, FallbackBackend)
