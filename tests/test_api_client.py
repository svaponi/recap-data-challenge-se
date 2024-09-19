import pytest

from app.api_client import APIClient


@pytest.mark.skip
def test_fetch_page():
    client = APIClient(
        "https://nookdtmzylu7w75p7atatnzom40zmdpz.lambda-url.eu-central-1.on.aws/invoices"
    )
    results, total_pages = client.fetch_page(1)
    assert results is not None
    assert total_pages is not None
