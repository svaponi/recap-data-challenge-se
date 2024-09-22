import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

from app.api_client import APIClient

_MAX_ERRORS = 3


def producer(queue: Queue, api_client: APIClient, max_workers: int):
    semaphore = threading.Semaphore(max_workers)
    errors = 0

    def fetch_page(_page):
        with semaphore:
            try:
                _results, _total_pages = api_client.fetch_page(_page)
                if _results:
                    for r in _results:
                        queue.put(r)
                return _total_pages
            except Exception as e:
                print(f"Error fetching page {_page}: {e}")
                nonlocal errors
                if errors >= _MAX_ERRORS:
                    raise RuntimeError(f"Too many errors, aborting") from e
                errors += 1
                return -1

    page = 1
    total_pages = None
    futures = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while total_pages is None or total_pages >= page:
            # Submit the fetch_page task to the thread pool
            future = executor.submit(fetch_page, page)
            futures.append(future)
            page += 1

            # If the total pages are not known, wait for at least one task to complete
            if total_pages is None and len(futures) >= max_workers:
                total_pages = wait_for_first_completion(futures).result()

        # Ensure remaining tasks are completed
        for future in futures:
            future.result()

        # Signal the consumer that producer is done
        queue.put(None)


# Helper function to wait for the first completed future
def wait_for_first_completion(futures):
    while True:
        for future in futures:
            if future.done():
                return future
