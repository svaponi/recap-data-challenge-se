import requests

from app.api_model import ApiResponse, InvoiceItem


class APIClient:
    def __init__(self, endpoint_url, trace_id=None):
        assert endpoint_url, "missing endpoint_url"
        assert "?" not in endpoint_url, "invalid endpoint_url"
        self.endpoint_url = endpoint_url
        self.trace_id = trace_id

    def fetch_page(self, page) -> tuple[list[InvoiceItem], int]:
        assert page > 0, "Page must be a positive integer"

        params = {"page": page}
        if self.trace_id:
            params["trace_id"] = self.trace_id

        response = requests.get(self.endpoint_url, params=params)

        if response.status_code == 404:
            return [], False

        if response.ok:
            data = response.json()
            model = ApiResponse(**data)
            return model.body.data, model.body.total_pages

        # todo handle other errors, retry, etc

        raise RuntimeError(f"Failed to fetch page {page}: {response.text}")
