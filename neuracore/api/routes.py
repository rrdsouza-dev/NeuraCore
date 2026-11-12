"""Rotas HTTP da API pública inicial."""

import secrets

from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import Response

from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest, InferenceResponse
from neuracore.inference.sessions import Session, SessionMessage, SessionStore
from neuracore.monitoring.diagnostics import DiagnosticsSnapshot, collect_diagnostics
from neuracore.monitoring.metrics import (
    inference_duration_seconds,
    inference_requests,
    render_metrics,
)
from neuracore.queue.engine import InferenceQueue, QueueFullError, QueueStatus
from neuracore.resources.monitor import ResourceMonitor, ResourceSnapshot
from neuracore.scheduler.admission import AdmissionPolicy, AdmissionRejectedError


def create_router(
    engine: InferenceEngine,
    resource_monitor: ResourceMonitor | None = None,
    inference_queue: InferenceQueue | None = None,
    session_store: SessionStore | None = None,
    admission_policy: AdmissionPolicy | None = None,
    api_key: str | None = None,
) -> APIRouter:
    """Cria as rotas com o motor de inferência injetado."""

    def authorize(x_api_key: str | None = Header(default=None)) -> None:
        if api_key is not None and (
            x_api_key is None or not secrets.compare_digest(x_api_key, api_key)
        ):
            raise HTTPException(status_code=401, detail="Chave de API inválida")

    router = APIRouter(dependencies=[Depends(authorize)])
    monitor = resource_monitor or ResourceMonitor()
    queue = inference_queue
    sessions = session_store or SessionStore()
    admission = admission_policy or AdmissionPolicy()

    @router.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/health/resources", response_model=ResourceSnapshot)
    async def health_resources() -> ResourceSnapshot:
        return monitor.snapshot()

    @router.get("/health/queue", response_model=QueueStatus)
    async def health_queue() -> QueueStatus:
        return (
            queue.status()
            if queue is not None
            else QueueStatus(pending=0, capacity=0, workers=0, running=False)
        )

    @router.get("/diagnostics", response_model=DiagnosticsSnapshot)
    async def diagnostics() -> DiagnosticsSnapshot:
        return collect_diagnostics(resource_monitor=monitor)

    @router.get("/metrics", include_in_schema=False)
    async def metrics() -> Response:
        return Response(content=render_metrics(), media_type="text/plain; version=0.0.4")

    @router.post("/v1/inference", response_model=InferenceResponse)
    async def inference(request: InferenceRequest) -> InferenceResponse:
        inference_requests.inc()
        with inference_duration_seconds.time():
            try:
                admission.admit(monitor.snapshot())
            except AdmissionRejectedError as error:
                raise HTTPException(status_code=503, detail=str(error)) from error
            if request.session_id is not None:
                try:
                    sessions.append(
                        request.session_id,
                        SessionMessage(role="user", content=request.prompt),
                    )
                except KeyError as error:
                    raise HTTPException(status_code=404, detail=str(error)) from error
            try:
                response = (
                    await queue.submit(request)
                    if queue is not None
                    else await engine.generate(request)
                )
            except QueueFullError as error:
                raise HTTPException(status_code=429, detail=str(error)) from error
            if request.session_id is not None:
                sessions.append(
                    request.session_id,
                    SessionMessage(role="assistant", content=response.text),
                )
            return response

    @router.post("/v1/sessions", response_model=Session, status_code=201)
    async def create_session() -> Session:
        return sessions.create()

    @router.get("/v1/sessions/{session_id}", response_model=Session)
    async def get_session(session_id: str) -> Session:
        try:
            return sessions.get(session_id)
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    @router.post("/v1/sessions/{session_id}/messages", response_model=Session)
    async def append_session_message(session_id: str, message: SessionMessage) -> Session:
        try:
            return sessions.append(session_id, message)
        except KeyError as error:
            raise HTTPException(status_code=404, detail=str(error)) from error

    return router
