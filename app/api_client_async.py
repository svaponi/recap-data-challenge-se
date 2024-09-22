from typing import Tuple, List

import aiohttp

from app.api_model import InvoiceItem, ApiResponse


class APIClientAsync:
    def __init__(self, endpoint_url, trace_id=None):
        assert endpoint_url, "missing endpoint_url"
        assert "?" not in endpoint_url, "invalid endpoint_url"
        self.endpoint_url = endpoint_url
        self.trace_id = trace_id
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, page: int) -> Tuple[List[InvoiceItem], int]:
        assert self.session, "no session yet"
        assert page > 0, "Page must be a positive integer"
        params = {"page": page}
        if self.trace_id:
            params["trace_id"] = self.trace_id
        async with self.session.get(self.endpoint_url, params=params) as response:
            if response.status == 404:
                return [], 0

            if response.status == 200:
                data = await response.json()
                model = ApiResponse(**data)
                return model.body.data, model.body.total_pages

            raise RuntimeError(f"Failed to fetch page {page}: {response.text()}")
