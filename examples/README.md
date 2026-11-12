# Exemplos

## Requisição mínima

Com a API em execução:

```powershell
$body = @{ model = "llama3"; prompt = "Responda com uma frase" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8000/v1/inference `
  -ContentType "application/json" -Body $body
```

Com autenticação habilitada, acrescente `-Headers @{ "X-API-Key" = $env:NEURACORE_API_KEY }`.
