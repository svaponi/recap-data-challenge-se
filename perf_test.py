import asyncio
import json
import time
from http.client import HTTPResponse
from urllib.request import urlopen

_SERVER = "http://127.0.0.1:8007"
_ENDPOINT_DATA = f"{_SERVER}/invoices"
_ENDPOINT_STATS = f"{_SERVER}/stats"


def run_threads(max_workers):
    from app.api_client import APIClient
    from app.processor import process

    client = APIClient(_ENDPOINT_DATA, f"run_threads_{str(max_workers).zfill(2)}")
    results = process(client, max_workers=max_workers)
    return results


if __name__ == "__main__":
    # check if server is running
    urlopen(_ENDPOINT_STATS, timeout=10)

    concurrency = [4, 8, 16, 32, 64]
    for max_workers in concurrency:
        start = time.perf_counter()
        results = run_threads(max_workers=max_workers)
        end = time.perf_counter()
        elapsed = end - start
        print(f"{max_workers=} {elapsed=} {len(results)=}")

    r: HTTPResponse = urlopen(_ENDPOINT_STATS, timeout=1)
    data = json.loads(r.read())
    data = json.dumps(data, indent=2)
    print(f"{r.status=}")
    print(data)
