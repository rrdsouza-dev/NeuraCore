from json import loads

import httpx

from neuracore.backends.ollama import OllamaBackend


async def test_ollama_generate_uses_expected_payload() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/generate"
        assert loads(request.content) == {"model": "llama3", "prompt": "Oi", "stream": False}
        return httpx.Response(200, json={"response": "Olá!"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://ollama") as client:
        result = await OllamaBackend(client=client).generate("Oi", model="llama3")

    assert result == "Olá!"
