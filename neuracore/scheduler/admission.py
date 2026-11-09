"""Política inicial para impedir novas cargas sob pressão de recursos."""

from dataclasses import dataclass

from neuracore.resources.monitor import ResourceSnapshot


class AdmissionRejectedError(RuntimeError):
    """Indica que os recursos atuais não suportam uma nova solicitação."""


@dataclass(frozen=True)
class AdmissionPolicy:
    """Limites simples de CPU e memória do sistema."""

    max_cpu_percent: float = 95.0
    max_memory_percent: float = 95.0

    def admit(self, snapshot: ResourceSnapshot) -> None:
        """Aceita o uso atual ou rejeita com uma justificativa clara."""
        if snapshot.cpu_percent > self.max_cpu_percent:
            raise AdmissionRejectedError("CPU acima do limite de admissão")
        if snapshot.memory_percent > self.max_memory_percent:
            raise AdmissionRejectedError("Memória acima do limite de admissão")
