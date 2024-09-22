import asyncio
from asyncio import Queue

import pytest

from app.api_model import InvoiceItem
from app.consumer_async import consumer


@pytest.mark.asyncio
async def test_consumer():
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

    queue_in = Queue()
    queue_out = Queue()
    task = asyncio.create_task(consumer(queue_in, queue_out))

    for item in data:
        await queue_in.put(item)
    await queue_in.put(None)

    await task
    results = [queue_out.get_nowait() for _ in range(queue_out.qsize())]

    # Verify the aggregation result
    it = iter(results)
    assert next(it, None) == ((2023, 9), "client_1", 300.0)
    assert next(it, None) == ((2023, 9), "client_2", 250.0)
    assert next(it, None) == ((2023, 9), "client_3", 150.0)
    assert next(it, None) == ((2023, 10), "client_2", 275.0)
    assert next(it, None) is None
