import asyncio
import json
import time
from http.client import HTTPResponse
from urllib.request import urlopen

import psutil

_SERVER = "http://127.0.0.1:8007"
_ENDPOINT_DATA = f"{_SERVER}/invoices"
_ENDPOINT_STATS = f"{_SERVER}/stats"


def run_threads(max_workers):
    from app.api_client import APIClient
    from app.processor import process

    client = APIClient(_ENDPOINT_DATA, f"run_threads_{str(max_workers).zfill(2)}")
    return process(client, max_workers=max_workers)


def run_async(max_workers):
    from app.api_client_async import APIClientAsync
    from app.processor_async import process

    client = APIClientAsync(_ENDPOINT_DATA, f"run_async_{str(max_workers).zfill(2)}")
    return asyncio.run(process(client, max_workers=max_workers))


if __name__ == "__main__":
    # check if server is running
    urlopen(_ENDPOINT_STATS, timeout=10)

    process = psutil.Process()
    print(f"{process.pid=}")

    run_funcs = [run_async, run_threads]
    concurrency = [4, 8, 16, 32, 64]
    for run_func in run_funcs:
        for max_workers in concurrency:
            start = time.perf_counter()
            results = run_func(max_workers=max_workers)
            end = time.perf_counter()
            elapsed = end - start
            rss = round(process.memory_info().rss / 1024**2, 3)
            cpu_percent = process.cpu_percent()
            print(
                f"{run_func.__name__} {max_workers=} {elapsed=} {len(results)=} {rss=}MB {cpu_percent=}%"
            )

    r: HTTPResponse = urlopen(_ENDPOINT_STATS, timeout=1)
    data = json.loads(r.read())
    data = json.dumps(data, indent=2)
    print(f"{r.status=}")
    print(data)
