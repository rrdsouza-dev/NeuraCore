# NeuraCore

O NeuraCore é uma base em Python para executar modelos de IA localmente de forma organizada e extensível. A ideia é ficar entre as aplicações e os backends de inferência, cuidando das partes comuns como fila, recursos, métricas e recuperação de falhas.

## Status

O projeto ainda está no começo. Já existe uma API funcional, integração inicial com o Ollama, fila assíncrona, prioridades, limite de capacidade, métricas, monitoramento básico, retry e testes automatizados. Os componentes mais avançados ainda estão sendo construídos.

## Architecture

O pacote `neuracore` é dividido por responsabilidade: `core`, `inference`, `backends`, `scheduler`, `resources`, `queue`, `monitoring`, `recovery`, `api`, `policies` e `cli`. O Ollama é o primeiro backend. Novos backends podem implementar o contrato assíncrono definido em `backends.base`.

## Planned components

- Abstração para backends e gerenciamento do ciclo de vida dos modelos
- Monitoramento de recursos e escalonamento
- Filas assíncronas e sessões de inferência
- Saúde da aplicação, métricas, tracing, diagnósticos e recuperação
- Serviço FastAPI e CLI com Typer

## Technologies and requirements

Python 3.11 ou superior, Ollama, FastAPI, Pydantic, httpx, psutil, Typer, Rich, Prometheus/OpenTelemetry, pytest, Ruff e Mypy.

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

O Ollama é o primeiro backend. A instalação e os modelos ficam por conta do desenvolvedor; o NeuraCore não baixa modelos automaticamente.

## Development

```powershell
pytest
ruff check .
ruff format --check .
mypy
```

As configurações usam variáveis de ambiente com o prefixo `NEURACORE_`. Por padrão, o Ollama é procurado em `http://localhost:11434`.

Para configurar um fallback compatível com OpenAI, defina `NEURACORE_FALLBACK_BASE_URL` e, se necessário, `NEURACORE_FALLBACK_API_KEY`.

## Roadmap

1. Ampliar o contrato de inferência e o transporte do Ollama.
2. Evoluir o scheduler e o controle de recursos.
3. Adicionar sessões, tracing, diagnósticos e mecanismos de recuperação mais completos.

## Contributing

As orientações estão em [CONTRIBUTING.md](CONTRIBUTING.md). Prefira mudanças pequenas, testes, tipagem e mensagens de commit em português.
