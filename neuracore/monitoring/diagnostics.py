"""Diagnóstico operacional sem exposição de segredos."""

from pydantic import BaseModel

from neuracore import __version__
from neuracore.core.config import Settings
from neuracore.resources.hardware import HardwareDetector, HardwareSnapshot
from neuracore.resources.monitor import ResourceMonitor, ResourceSnapshot


class DiagnosticsSnapshot(BaseModel):
    """Informações úteis para suporte e inspeção local."""

    version: str
    inference_backend: str
    ollama_base_url: str
    resources: ResourceSnapshot
    hardware: HardwareSnapshot


def collect_diagnostics(
    settings: Settings | None = None,
    resource_monitor: ResourceMonitor | None = None,
    hardware_detector: HardwareDetector | None = None,
) -> DiagnosticsSnapshot:
    """Monta um diagnóstico sem incluir tokens ou chaves de API."""
    runtime_settings = settings or Settings()
    return DiagnosticsSnapshot(
        version=__version__,
        inference_backend=runtime_settings.inference_backend,
        ollama_base_url=runtime_settings.ollama_base_url,
        resources=(resource_monitor or ResourceMonitor()).snapshot(),
        hardware=(hardware_detector or HardwareDetector()).snapshot(),
    )
