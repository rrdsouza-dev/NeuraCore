"""Backend para servidores que expõem a API compatível com OpenAI."""

from typing import cast

import httpx

from neuracore.backends.base import InferenceBackend


class OpenAICompatibleBackend(InferenceBackend):
    """Cliente mínimo para o endpoint `/v1/chat/completions`."""

    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self._client = client

    async def generate(self, prompt: str, *, model: str) -> str:
        """Envia uma mensagem única e retorna o conteúdo da primeira escolha."""
        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }
        if self._client is None:
            async with httpx.AsyncClient(base_url=self.base_url) as client:
                response = await client.post("/v1/chat/completions", json=payload, headers=headers)
        else:
            response = await self._client.post(
                "/v1/chat/completions", json=payload, headers=headers
            )
        response.raise_for_status()
        data = response.json()
        return cast(str, data["choices"][0]["message"]["content"])
