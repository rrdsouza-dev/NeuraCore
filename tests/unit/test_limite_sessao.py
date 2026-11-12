import pytest

from neuracore.inference.sessions import SessionMessage, SessionStore


def test_sessao_mantem_apenas_as_mensagens_recentes() -> None:
    store = SessionStore(max_messages=2)
    session = store.create()
    store.append(session.id, SessionMessage(role="user", content="um"))
    store.append(session.id, SessionMessage(role="user", content="dois"))
    store.append(session.id, SessionMessage(role="user", content="três"))

    assert [message.content for message in store.get(session.id).messages] == ["dois", "três"]


def test_limite_de_sessao_deve_ser_positivo() -> None:
    with pytest.raises(ValueError, match="limite de mensagens"):
        SessionStore(max_messages=0)
