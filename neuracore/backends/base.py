"""Contracts shared by inference backends."""

from abc import ABC, abstractmethod


class InferenceBackend(ABC):
    """Minimal asynchronous contract for a backend implementation."""

    @abstractmethod
    async def generate(self, prompt: str, *, model: str) -> str:
        """Generate a response for a prompt."""

