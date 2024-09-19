from app.api_client import APIClient
from app.api_model import InvoiceItem


def chunk_list(lst, chunk_size):
    # Loop over the list and create chunks of size `chunk_size`
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


class MockAPIClient(APIClient):

    def __init__(self, data=list[InvoiceItem], page_size=None):
        data = data or []
        page_size = page_size or 2
        self._pages = chunk_list(data, page_size)

    def fetch_page(self, page) -> tuple[list[InvoiceItem], int]:
        assert page > 0, "Page must be a positive integer"
        try:
            return self._pages[page - 1], len(self._pages)
        except:
            return [], len(self._pages)
