from fastapi.testclient import TestClient

from neuracore.api.server import create_app
from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return f"resposta: {prompt}"


def test_inferencia_associada_a_sessao_registra_duas_mensagens() -> None:
    with TestClient(create_app(InferenceEngine(BackendDeTeste()))) as client:
        session_id = client.post("/v1/sessions").json()["id"]
        response = client.post(
            "/v1/inference",
            json={"model": "teste", "prompt": "Olá", "session_id": session_id},
        )
        session = client.get(f"/v1/sessions/{session_id}").json()

    assert response.status_code == 200
    assert [message["role"] for message in session["messages"]] == ["user", "assistant"]
