import pytest

from neuracore.resources.monitor import ResourceSnapshot
from neuracore.scheduler.admission import AdmissionPolicy, AdmissionRejectedError


def test_admissao_aceita_recursos_disponiveis() -> None:
    snapshot = ResourceSnapshot(cpu_percent=40, memory_percent=50, memory_available_bytes=100)

    AdmissionPolicy().admit(snapshot)


def test_admissao_rejeita_memoria_alta() -> None:
    snapshot = ResourceSnapshot(cpu_percent=40, memory_percent=96, memory_available_bytes=10)

    with pytest.raises(AdmissionRejectedError, match="Memória"):
        AdmissionPolicy().admit(snapshot)
