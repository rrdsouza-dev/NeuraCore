"""Políticas básicas para ordenação da fila."""

from enum import StrEnum


class Priority(StrEnum):
    """Níveis de prioridade expostos na API."""

    ALTA = "alta"
    NORMAL = "normal"
    BAIXA = "baixa"

    @property
    def weight(self) -> int:
        """Converte o nível em peso para ordenação interna."""
        return {Priority.ALTA: 0, Priority.NORMAL: 1, Priority.BAIXA: 2}[self]
