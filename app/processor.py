import threading
from queue import Queue

from app.api_client import APIClient
from app.consumer import consumer
from app.model import ProcessorOut
from app.postprocessor import postprocess
from app.producer import producer


def process(api_client: APIClient, max_workers) -> list[ProcessorOut]:
    queue = Queue()
    result_queue = Queue()

    # Start producer and consumer threads
    producer_thread = threading.Thread(target=producer, args=(queue, api_client, max_workers))
    consumer_thread = threading.Thread(target=consumer, args=(queue, result_queue))

    producer_thread.start()
    consumer_thread.start()

    # Wait for both threads to finish
    producer_thread.join()
    consumer_thread.join()

    results = [result_queue.get_nowait() for _ in range(result_queue.qsize())]
    results = postprocess(results)
    return results
