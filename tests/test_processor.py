from app.api_model import InvoiceItem
from app.processor import process
from tests.api_client_mock import MockAPIClient


def test_process():
    data = [
        InvoiceItem(
            invoice_date="2023-09-01",
            contract_id="client_1",
            original_billing_amount=100,
        ),
        InvoiceItem(
            invoice_date="2023-09-05",
            contract_id="client_2",
            original_billing_amount=250,
        ),
        InvoiceItem(
            invoice_date="2023-09-10",
            contract_id="client_3",
            original_billing_amount=150,
        ),
        InvoiceItem(
            invoice_date="2023-09-15",
            contract_id="client_1",
            original_billing_amount=200,
        ),
        InvoiceItem(
            invoice_date="2023-10-01",
            contract_id="client_2",
            original_billing_amount=275,
        ),
    ]

    # Call fetch_all_pages with the mocked API client
    results = process(MockAPIClient(data=data, page_size=2), max_workers=2)

    # Verify the aggregation result
    results = sorted(results, key=lambda x: (x[0], x[1]))
    it = iter(results)
    assert next(it, None) == ((2023, 9), "client_1", 300.0, 0)
    assert next(it, None) == ((2023, 9), "client_2", 250.0, 0)
    assert next(it, None) == ((2023, 9), "client_3", 150.0, 0)
    assert next(it, None) == ((2023, 10), "client_1", 0, 300.0)
    assert next(it, None) == ((2023, 10), "client_2", 275.0, 0)
    assert next(it, None) == ((2023, 10), "client_3", 0, 150.0)
    assert next(it, None) is None
