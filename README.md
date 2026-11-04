# NeuraCore

NeuraCore is an open-source Python foundation for extensible local AI inference. It is intended to sit between applications and inference backends, providing clear boundaries for lifecycle, resources, scheduling, observability, and recovery.

## Status

Early-stage infrastructure. The current release establishes package boundaries, configuration, an Ollama backend contract, development tooling, and CI. Planned capabilities are not implemented yet.

## Architecture

The `neuracore` package is separated into `core`, `inference`, `backends`, `scheduler`, `resources`, `queue`, `monitoring`, `recovery`, `api`, `policies`, and `cli`. Ollama is the first backend boundary; other backends can implement the shared asynchronous contract in `backends.base`.

## Planned components

- Backend abstraction and model lifecycle management
- Resource awareness and scheduling
- Asynchronous queues and inference sessions
- Health, metrics, tracing, diagnostics, and recovery
- FastAPI service and Typer CLI

## Technologies and requirements

Python 3.11+, Ollama (optional at development time), FastAPI, Pydantic, httpx, psutil, Typer, Rich, Prometheus/OpenTelemetry, pytest, Ruff, and Mypy.

## Installation

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

Ollama is the initial inference target. Install and run it separately when needed; this project does not download models automatically.

## Development

```powershell
pytest
ruff check .
ruff format --check .
mypy
```

Configuration uses `NEURACORE_` environment variables, with `NEURACORE_OLLAMA_BASE_URL` defaulting to `http://localhost:11434`.

## Roadmap

1. Define inference requests and implement the Ollama transport.
2. Add API routes and health/metrics endpoints.
3. Introduce queueing, resource-aware admission, scheduling, and recovery incrementally.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Use focused changes, tests, type hints, and Conventional Commits.
