"""Políticas básicas para ordenação da fila."""

from enum import Enum


class Priority(str, Enum):
    """Níveis de prioridade expostos na API."""

    ALTA = "alta"
    NORMAL = "normal"
    BAIXA = "baixa"

    @property
    def weight(self) -> int:
        """Converte o nível em peso para ordenação interna."""
        return {Priority.ALTA: 0, Priority.NORMAL: 1, Priority.BAIXA: 2}[self]
