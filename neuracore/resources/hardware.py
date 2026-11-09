"""Descoberta opcional de GPUs NVIDIA disponíveis."""

from pydantic import BaseModel, Field


class GpuInfo(BaseModel):
    """Informações básicas de uma GPU."""

    index: int
    name: str
    memory_total_bytes: int


class HardwareSnapshot(BaseModel):
    """Capacidades detectadas sem exigir GPU para o funcionamento do projeto."""

    nvidia_available: bool = False
    gpus: list[GpuInfo] = Field(default_factory=list)


class HardwareDetector:
    """Consulta NVML quando o driver e a biblioteca estão disponíveis."""

    def snapshot(self) -> HardwareSnapshot:
        """Retorna GPUs NVIDIA ou uma resposta vazia em máquinas sem NVIDIA."""
        try:
            import pynvml
        except ImportError:
            return HardwareSnapshot()

        try:
            pynvml.nvmlInit()
            devices = []
            for index in range(pynvml.nvmlDeviceGetCount()):
                handle = pynvml.nvmlDeviceGetHandleByIndex(index)
                name = pynvml.nvmlDeviceGetName(handle)
                if isinstance(name, bytes):
                    name = name.decode("utf-8", errors="replace")
                memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
                devices.append(GpuInfo(index=index, name=name, memory_total_bytes=memory.total))
            return HardwareSnapshot(nvidia_available=bool(devices), gpus=devices)
        except Exception:
            return HardwareSnapshot()
        finally:
            try:
                pynvml.nvmlShutdown()
            except Exception:
                pass
