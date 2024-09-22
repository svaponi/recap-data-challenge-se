import asyncio
from typing import List

from app.model import ProcessorOut
from app.postprocessor import postprocess
from app.api_client_async import APIClientAsync
from app.consumer_async import consumer
from app.producer_async import producer


async def process(api_client: APIClientAsync, max_workers: int) -> List[ProcessorOut]:
    queue = asyncio.Queue()
    result_queue = asyncio.Queue()

    # Start and await producer and consumer in parallel
    async with api_client as client:
        await asyncio.gather(
            producer(queue, client, max_workers), consumer(queue, result_queue)
        )

    # Collect results from the result queue
    _results = [result_queue.get_nowait() for _ in range(result_queue.qsize())]
    _results = postprocess(_results)
    return _results
