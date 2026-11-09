import httpx

from neuracore.backends.openai_compatible import OpenAICompatibleBackend


async def test_backend_compativel_envia_formato_de_chat() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/v1/chat/completions"
        assert request.headers["authorization"] == "Bearer segredo"
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Resposta"}}]},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport, base_url="http://servidor") as client:
        backend = OpenAICompatibleBackend(
            "http://servidor/",
            api_key="segredo",
            client=client,
        )
        result = await backend.generate("Olá", model="modelo")

    assert result == "Resposta"
