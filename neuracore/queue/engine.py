"""Fila FIFO assíncrona para solicitações de inferência."""

import asyncio

from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest, InferenceResponse


class QueueFullError(RuntimeError):
    """Indica que a fila atingiu o limite configurado."""


class InferenceQueue:
    """Processa solicitações em ordem usando um único worker."""

    def __init__(self, engine: InferenceEngine, max_size: int = 100) -> None:
        self.engine = engine
        if max_size < 1:
            raise ValueError("O tamanho máximo da fila deve ser positivo")
        self._jobs: asyncio.Queue[tuple[InferenceRequest, asyncio.Future[InferenceResponse]]] = (
            asyncio.Queue(maxsize=max_size)
        )
        self._worker: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Inicia o worker da fila."""
        if self._worker is None:
            self._worker = asyncio.create_task(self._process())

    async def stop(self) -> None:
        """Encerra o worker e aguarda sua finalização."""
        if self._worker is not None:
            self._worker.cancel()
            await asyncio.gather(self._worker, return_exceptions=True)
            self._worker = None

    async def submit(self, request: InferenceRequest) -> InferenceResponse:
        """Adiciona uma solicitação e aguarda sua resposta."""
        if self._worker is None:
            raise RuntimeError("A fila não foi iniciada")
        loop = asyncio.get_running_loop()
        result: asyncio.Future[InferenceResponse] = loop.create_future()
        try:
            self._jobs.put_nowait((request, result))
        except asyncio.QueueFull as error:
            raise QueueFullError("A fila de inferência está cheia") from error
        return await result

    async def _process(self) -> None:
        while True:
            request, result = await self._jobs.get()
            try:
                result.set_result(await self.engine.generate(request))
            except Exception as error:
                result.set_exception(error)
            finally:
                self._jobs.task_done()
