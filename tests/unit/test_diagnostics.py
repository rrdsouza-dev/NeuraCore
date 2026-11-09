from neuracore.core.config import Settings
from neuracore.monitoring.diagnostics import collect_diagnostics
from neuracore.resources.hardware import HardwareDetector, HardwareSnapshot
from neuracore.resources.monitor import ResourceMonitor, ResourceSnapshot


class MonitorFalso(ResourceMonitor):
    def snapshot(self) -> ResourceSnapshot:
        return ResourceSnapshot(cpu_percent=1, memory_percent=2, memory_available_bytes=3)


class HardwareFalso(HardwareDetector):
    def snapshot(self) -> HardwareSnapshot:
        return HardwareSnapshot()


def test_diagnostico_nao_expoe_chave_de_api() -> None:
    snapshot = collect_diagnostics(
        Settings(fallback_api_key="nao-deve-aparecer"), MonitorFalso(), HardwareFalso()
    )

    assert snapshot.version == "0.1.0"
    assert snapshot.resources.memory_available_bytes == 3
    assert "nao-deve-aparecer" not in snapshot.model_dump_json()
