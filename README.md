# NeuraCore

O NeuraCore é uma base em Python para executar modelos de IA localmente de forma organizada e extensível. A ideia é ficar entre as aplicações e os backends de inferência, cuidando das partes comuns como fila, recursos, métricas e recuperação de falhas.

## Status

MVP operacional concluído. A base já está pronta para desenvolvimento e uso local, com API funcional, integração com Ollama e backends compatíveis com OpenAI, fila assíncrona, prioridades, limite de capacidade, sessões, persistência SQLite, métricas, tracing, diagnósticos, retry, fallback e testes automatizados.

## Arquitetura

O pacote `neuracore` é dividido por responsabilidade: `core`, `inference`, `backends`, `scheduler`, `resources`, `queue`, `monitoring`, `recovery`, `api`, `policies` e `cli`. O Ollama é o primeiro backend. Novos backends podem implementar o contrato assíncrono definido em `backends.base`.

## Componentes disponíveis

- Abstração para backends e gerenciamento do ciclo de vida
- Monitoramento de recursos e política de admissão
- Filas assíncronas com prioridades e múltiplos workers
- Sessões em memória ou SQLite com limite de histórico
- Saúde, métricas Prometheus, tracing OpenTelemetry e diagnósticos
- Retry seletivo, circuit breaker e fallback
- Serviço FastAPI e CLI com Typer

## Tecnologias e requisitos

Python 3.11 ou superior, Ollama, FastAPI, Pydantic, httpx, psutil, Typer, Rich, Prometheus/OpenTelemetry, pytest, Ruff e Mypy.

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -e ".[dev]"
```

O Ollama é o primeiro backend. A instalação e os modelos ficam por conta do desenvolvedor; o NeuraCore não baixa modelos automaticamente.

## Desenvolvimento

```powershell
pytest
ruff check .
ruff format --check .
mypy
python -m pip_audit
python -m bandit -r neuracore -q
```

As configurações usam variáveis de ambiente com o prefixo `NEURACORE_`. Por padrão, o Ollama é procurado em `http://localhost:11434`.

Para configurar um fallback compatível com OpenAI, defina `NEURACORE_FALLBACK_BASE_URL` e, se necessário, `NEURACORE_FALLBACK_API_KEY`.

Em ambientes que exigem proteção, defina `NEURACORE_API_KEY`. Nesse caso, envie a mesma chave no cabeçalho `X-API-Key`.

## Executando a API

```powershell
neuracore serve
```

Endpoints principais:

- `GET /health` — verifica se a aplicação está respondendo.
- `GET /health/resources` — mostra CPU e memória disponíveis.
- `GET /health/queue` — mostra capacidade e workers ativos.
- `GET /metrics` — expõe métricas para o Prometheus.
- `POST /v1/inference` — envia uma solicitação de inferência.

Exemplo de requisição:

```json
{
  "model": "llama3",
  "prompt": "Explique filas assíncronas em poucas palavras",
  "priority": "normal"
}
```

A fila tem limite de capacidade, aceita as prioridades `alta`, `normal` e `baixa` e responde com HTTP 429 quando está cheia.

## Verificação antes de publicar

```powershell
python -m pip check
python -m pip_audit
python -m bandit -r neuracore -q
ruff check .
mypy
pytest
```

O projeto não baixa modelos automaticamente. Antes de usar inferência, deixe o Ollama em execução e confirme que o modelo configurado está disponível.

## Próximas evoluções

1. Testes de carga contínuos em ambiente de implantação.
2. Integrações automatizadas com Ollama em execução.
3. Painéis de observabilidade e exemplos de implantação.

## Contribuindo

As orientações estão em [CONTRIBUTING.md](CONTRIBUTING.md). Prefira mudanças pequenas, testes, tipagem e mensagens de commit em português.
