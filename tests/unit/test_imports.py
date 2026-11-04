from neuracore import __version__
from neuracore.backends.ollama import OllamaBackend
from neuracore.core.config import Settings


def test_package_imports() -> None:
    assert __version__ == "0.1.0"
    assert OllamaBackend().settings.ollama_base_url == "http://localhost:11434"


def test_settings_override(monkeypatch) -> None:
    monkeypatch.setenv("NEURACORE_APP_NAME", "TestCore")
    assert Settings().app_name == "TestCore"

