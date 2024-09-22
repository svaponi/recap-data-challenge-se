import collections
import json
import multiprocessing
import os
import time

import flask

app = flask.Flask(__name__)
_collector = collections.defaultdict(list)
_lock = multiprocessing.Lock()


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


_NO_OF_PAGES = 1_000


@app.get("/invoices")
def get_invoices():
    trace_id = flask.request.args.get("trace_id")
    if trace_id:
        with _lock:
            _collector[trace_id].append(time.time())
    page = flask.request.args.get("page", 1)
    page = int(page)
    if 10 < page <= _NO_OF_PAGES:
        page = (page - 1) % 10 + 1
    path = os.path.join(os.path.dirname(__file__), f"testdata", f"page{page}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            data["body"]["total_pages"] = _NO_OF_PAGES
            return data, 200, {"content-type": "application/json"}
    return {
        "status_code": 200,
        "body": {"data": [], "total_pages": _NO_OF_PAGES, "page": page},
    }


if __name__ == "__main__":
    app.run(port=8007)
