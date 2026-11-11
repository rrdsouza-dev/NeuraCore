def test_sessoes_podem_ser_persistidas_em_sqlite(tmp_path) -> None:
    from neuracore.inference.sessions import SessionMessage, SQLiteSessionStore

    path = str(tmp_path / "sessoes.db")
    first = SQLiteSessionStore(path)
    session = first.create()
    first.append(session.id, SessionMessage(role="user", content="persistir"))

    second = SQLiteSessionStore(path)

    assert second.get(session.id).messages[0].content == "persistir"
