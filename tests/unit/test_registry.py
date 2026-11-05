import pytest

from neuracore.backends.base import InferenceBackend
from neuracore.core.registry import BackendRegistry
from neuracore.inference.router import BackendRouter


class BackendFalso(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return prompt


def test_registro_e_roteador_selecionam_backend() -> None:
    backend = BackendFalso()
    registry = BackendRegistry()
    registry.register("falso", backend)

    assert BackendRouter(registry).select("falso") is backend


def test_registro_rejeita_backend_desconhecido() -> None:
    with pytest.raises(ValueError, match="não registrado"):
        BackendRegistry().get("inexistente")
