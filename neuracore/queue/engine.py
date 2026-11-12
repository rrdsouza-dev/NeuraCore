"""Fila FIFO assíncrona para solicitações de inferência."""

import asyncio

from pydantic import BaseModel

from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest, InferenceResponse


class QueueFullError(RuntimeError):
    """Indica que a fila atingiu o limite configurado."""


class QueueStatus(BaseModel):
    """Estado operacional atual da fila."""

    pending: int
    capacity: int
    workers: int
    running: bool


class InferenceQueue:
    """Processa solicitações em ordem usando um único worker."""

    def __init__(self, engine: InferenceEngine, max_size: int = 100, workers: int = 1) -> None:
        self.engine = engine
        if max_size < 1:
            raise ValueError("O tamanho máximo da fila deve ser positivo")
        if workers < 1:
            raise ValueError("A quantidade de workers deve ser positiva")
        self._jobs: asyncio.PriorityQueue[
            tuple[int, int, InferenceRequest, asyncio.Future[InferenceResponse]]
        ] = asyncio.PriorityQueue(maxsize=max_size)
        self._worker_tasks: list[asyncio.Task[None]] = []
        self._worker_count = workers
        self._sequence = 0

    async def start(self) -> None:
        """Inicia o worker da fila."""
        if not self._worker_tasks:
            self._worker_tasks = [
                asyncio.create_task(self._process()) for _ in range(self._worker_count)
            ]

    async def stop(self) -> None:
        """Encerra o worker e aguarda sua finalização."""
        if self._worker_tasks:
            self._reject_pending_jobs()
            for worker in self._worker_tasks:
                worker.cancel()
            await asyncio.gather(*self._worker_tasks, return_exceptions=True)
            self._worker_tasks = []

    def _reject_pending_jobs(self) -> None:
        while True:
            try:
                _, _, _, result = self._jobs.get_nowait()
            except asyncio.QueueEmpty:
                return
            if not result.done():
                result.set_exception(RuntimeError("A fila foi encerrada"))
            self._jobs.task_done()

    async def submit(self, request: InferenceRequest) -> InferenceResponse:
        """Adiciona uma solicitação e aguarda sua resposta."""
        if not self._worker_tasks:
            raise RuntimeError("A fila não foi iniciada")
        loop = asyncio.get_running_loop()
        result: asyncio.Future[InferenceResponse] = loop.create_future()
        try:
            self._jobs.put_nowait((request.priority.weight, self._sequence, request, result))
            self._sequence += 1
        except asyncio.QueueFull as error:
            raise QueueFullError("A fila de inferência está cheia") from error
        return await result

    def status(self) -> QueueStatus:
        """Retorna o estado sem alterar a fila."""
        return QueueStatus(
            pending=self._jobs.qsize(),
            capacity=self._jobs.maxsize,
            workers=self._worker_count,
            running=bool(self._worker_tasks),
        )

    async def _process(self) -> None:
        while True:
            _, _, request, result = await self._jobs.get()
            try:
                result.set_result(await self.engine.generate(request))
            except asyncio.CancelledError:
                if not result.done():
                    result.set_exception(RuntimeError("A fila foi encerrada"))
                raise
            except Exception as error:
                result.set_exception(error)
            finally:
                self._jobs.task_done()
