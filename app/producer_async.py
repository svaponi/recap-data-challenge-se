import asyncio

from app.api_client_async import APIClientAsync


async def producer(queue: asyncio.Queue, api_client: APIClientAsync, max_workers: int):
    semaphore = asyncio.Semaphore(max_workers)

    async def fetch_page(_page):
        async with semaphore:
            try:
                _results, _total_pages = await api_client.fetch_page(_page)
                if _results:
                    for r in _results:
                        await queue.put(r)
                return _total_pages
            except Exception as e:
                print(f"Error fetching page {_page}: {e}")
                return -1

    page = 1
    total_pages = None
    tasks = []

    while total_pages is None or total_pages >= page:
        tasks.append(asyncio.create_task(fetch_page(page)))
        page += 1

        if total_pages is None and len(tasks) >= max_workers:
            done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for t in done:
                total_pages = t.result()

    # Ensure remaining tasks are finished
    await asyncio.gather(*tasks)

    # Signal the consumer that producer is done
    await queue.put(None)
