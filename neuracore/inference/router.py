"""Roteamento explícito por nome de backend."""

from neuracore.backends.base import InferenceBackend
from neuracore.core.registry import BackendRegistry


class BackendRouter:
    """Seleciona somente o backend solicitado, sem heurísticas."""

    def __init__(self, registry: BackendRegistry) -> None:
        self.registry = registry

    def select(self, name: str) -> InferenceBackend:
        """Retorna o backend registrado para `name`."""
        return self.registry.get(name)
