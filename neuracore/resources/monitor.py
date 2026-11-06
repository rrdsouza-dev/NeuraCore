"""Leitura básica de recursos disponíveis no sistema."""

from pydantic import BaseModel
import psutil


class ResourceSnapshot(BaseModel):
    """Instantâneo dos recursos necessários para decisões futuras."""

    cpu_percent: float
    memory_percent: float
    memory_available_bytes: int


class ResourceMonitor:
    """Coleta recursos sem alocar ou gerenciar cargas."""

    def snapshot(self) -> ResourceSnapshot:
        """Retorna o uso atual de CPU e memória do sistema."""
        memory = psutil.virtual_memory()
        return ResourceSnapshot(
            cpu_percent=psutil.cpu_percent(interval=None),
            memory_percent=memory.percent,
            memory_available_bytes=memory.available,
        )
