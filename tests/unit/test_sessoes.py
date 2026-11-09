import pytest

from neuracore.inference.sessions import SessionMessage, SessionStore


def test_store_cria_e_atualiza_sessao() -> None:
    store = SessionStore()
    session = store.create()
    store.append(session.id, SessionMessage(role="user", content="Olá"))

    assert store.get(session.id).messages[0].content == "Olá"


def test_store_rejeita_sessao_desconhecida() -> None:
    with pytest.raises(KeyError, match="Sessão não encontrada"):
        SessionStore().get("inexistente")
