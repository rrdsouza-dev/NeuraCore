"""Registro simples para componentes nomeados."""

from neuracore.backends.base import InferenceBackend


class BackendRegistry:
    """Mantém os backends disponíveis sem acoplar o núcleo às implementações."""

    def __init__(self) -> None:
        self._backends: dict[str, InferenceBackend] = {}

    def register(self, name: str, backend: InferenceBackend) -> None:
        """Registra ou substitui um backend pelo nome informado."""
        self._backends[name] = backend

    def get(self, name: str) -> InferenceBackend:
        """Obtém um backend ou informa claramente que ele não existe."""
        try:
            return self._backends[name]
        except KeyError as error:
            raise ValueError(f"Backend não registrado: {name}") from error
