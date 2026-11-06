from typer.testing import CliRunner

from neuracore.cli.commands import app


def test_comando_version_exibe_versao() -> None:
    result = CliRunner().invoke(app, ["version"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "0.1.0"


def test_comando_serve_encaminha_opcoes(monkeypatch) -> None:
    chamada: dict[str, object] = {}

    def fake_run(application: str, **kwargs: object) -> None:
        chamada["application"] = application
        chamada.update(kwargs)

    monkeypatch.setattr("neuracore.cli.commands.uvicorn.run", fake_run)
    result = CliRunner().invoke(app, ["serve", "--host", "0.0.0.0", "--port", "9000", "--reload"])

    assert result.exit_code == 0
    assert chamada == {
        "application": "neuracore.api.server:app",
        "host": "0.0.0.0",
        "port": 9000,
        "reload": True,
    }
