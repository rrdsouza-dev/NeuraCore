from fastapi.testclient import TestClient

from neuracore.api.server import create_app
from neuracore.backends.base import InferenceBackend
from neuracore.inference.engine import InferenceEngine


class BackendDeTeste(InferenceBackend):
    async def generate(self, prompt: str, *, model: str) -> str:
        return prompt


def test_api_cria_consulta_e_atualiza_sessao() -> None:
    with TestClient(create_app(InferenceEngine(BackendDeTeste()))) as client:
        created = client.post("/v1/sessions")
        session_id = created.json()["id"]
        updated = client.post(
            f"/v1/sessions/{session_id}/messages",
            json={"role": "user", "content": "Olá"},
        )
        fetched = client.get(f"/v1/sessions/{session_id}")

    assert created.status_code == 201
    assert updated.status_code == 200
    assert fetched.json()["messages"][0]["content"] == "Olá"
