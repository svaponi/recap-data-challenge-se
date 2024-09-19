import time
from concurrent.futures import ThreadPoolExecutor, Future
from queue import Queue

from app.api_client import APIClient


def producer(queue: Queue, api_client: APIClient, max_workers: int):
    page = 1
    total_pages = 1_000

    def when_finished(f: Future):
        nonlocal total_pages
        try:
            results, total_pages = f.result()
            if results:
                for r in results:
                    queue.put(r)
        except Exception as e:
            print(f"Error fetching page: {e}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        while total_pages >= page:
            future = executor.submit(api_client.fetch_page, page)
            future.add_done_callback(when_finished)
            futures.append(future)
            time.sleep(0.1)
            page += 1

    # Signal the consumer that processing is done by adding a `None`
    queue.put(None)
