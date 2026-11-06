"""Comandos de linha de comando do NeuraCore."""

import typer
import uvicorn

app = typer.Typer(help="NeuraCore local inference infrastructure")


@app.command()
def version() -> None:
    """Exibe a versão instalada."""
    from neuracore import __version__

    typer.echo(__version__)


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", help="Endereço de escuta da API."),
    port: int = typer.Option(8000, min=1, max=65535, help="Porta de escuta da API."),
    reload: bool = typer.Option(False, help="Recarrega o processo ao alterar arquivos."),
) -> None:
    """Inicia a API HTTP do NeuraCore."""
    uvicorn.run("neuracore.api.server:app", host=host, port=port, reload=reload)
