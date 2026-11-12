# Documentação

O README na raiz reúne a instalação, a configuração e os endpoints principais.

## Operação

- Use `GET /health` para o liveness da aplicação.
- Use `GET /health/resources` e `GET /health/queue` para acompanhar capacidade.
- Use `GET /diagnostics` para um resumo operacional sem segredos.
- Exponha `GET /metrics` somente para a rede de monitoramento.
- Defina `NEURACORE_API_KEY` quando a API não estiver protegida por outra camada.

## Encerramento

O servidor encerra a fila, os clientes HTTP e o armazenamento de sessões no ciclo de vida da aplicação. Em produção, use um gerenciador de processos para reiniciar a aplicação após falhas e mantenha o SQLite em volume persistente.
