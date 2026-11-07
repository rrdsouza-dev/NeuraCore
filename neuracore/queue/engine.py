"""Fila FIFO assíncrona para solicitações de inferência."""

import asyncio

from neuracore.inference.engine import InferenceEngine
from neuracore.inference.requests import InferenceRequest, InferenceResponse


class InferenceQueue:
    """Processa solicitações em ordem usando um único worker."""

    def __init__(self, engine: InferenceEngine) -> None:
        self.engine = engine
        self._jobs: asyncio.Queue[tuple[InferenceRequest, asyncio.Future[InferenceResponse]]] = (
            asyncio.Queue()
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
        await self._jobs.put((request, result))
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
