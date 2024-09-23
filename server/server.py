import asyncio
import collections
import contextlib
import json
import os
import time

import aiofiles
import cachetools
import fastapi


@contextlib.asynccontextmanager
async def lifespan(*args):
    # warm up on startup
    for i in range(10):
        await _get_page(i)
    print("ready to serve")
    yield


app = fastapi.FastAPI(lifespan=lifespan)
_collector = collections.defaultdict(list)
_lock = asyncio.Lock()
_cur_dir = os.path.dirname(__file__)

_NO_OF_PAGES = 1_000
_CACHE = cachetools.LRUCache(maxsize=_NO_OF_PAGES)


async def _get_page(page) -> dict:
    if page in _CACHE:
        return _CACHE[page]
    path = os.path.join(_cur_dir, f"testdata", f"page{page}.json")
    if os.path.exists(path):
        async with aiofiles.open(path, "r") as f:
            contents = await f.read()
        data = json.loads(contents)
        data["body"]["total_pages"] = _NO_OF_PAGES
        _CACHE[page] = data
        return data
    return {
        "status_code": 200,
        "body": {"data": [], "total_pages": _NO_OF_PAGES, "page": page},
    }


@app.get("/stats")
def get_stats():
    resp = {}
    copy = dict(sorted(_collector.items()))
    _collector.clear()
    for trace_id, timestamps in copy.items():
        delta = max(timestamps) - min(timestamps)
        req_per_sec = len(timestamps) / delta
        resp[trace_id] = f"{round(req_per_sec, 2)} req/s, total {len(timestamps)}"
    return resp


@app.get("/invoices")
async def get_invoices(
    page: int = fastapi.Query(1),
    trace_id: str = fastapi.Query(None),
):
    if trace_id:
        async with _lock:
            _collector[trace_id].append(time.time())

    if 10 < page <= _NO_OF_PAGES:
        page_in_range = (page - 1) % 10 + 1
    else:
        page_in_range = page
    data = await _get_page(page_in_range)
    data["body"]["page"] = page
    return data


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", port=8007)
