from neuracore.inference.requests import InferenceRequest
from neuracore.queue.policies import Priority


def test_solicitacao_usa_prioridade_normal_por_padrao() -> None:
    request = InferenceRequest(model="teste", prompt="Olá")

    assert request.priority is Priority.NORMAL


def test_solicitacao_aceita_prioridade_alta() -> None:
    request = InferenceRequest(model="teste", prompt="Urgente", priority="alta")

    assert request.priority is Priority.ALTA
