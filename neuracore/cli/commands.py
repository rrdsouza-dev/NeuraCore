"""Initial CLI commands."""

import typer

app = typer.Typer(help="NeuraCore local inference infrastructure")


@app.command()
def version() -> None:
    """Show the installed version."""
    from neuracore import __version__

    typer.echo(__version__)

