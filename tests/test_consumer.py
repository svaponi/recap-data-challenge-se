import threading
from queue import Queue

from app.api_model import InvoiceItem
from app.consumer import consumer


def test_consumer():
    data = [
        InvoiceItem(invoice_date='2023-09-01', contract_id='client_1', original_billing_amount=100),
        InvoiceItem(invoice_date='2023-09-05', contract_id='client_2', original_billing_amount=250),
        InvoiceItem(invoice_date='2023-09-10', contract_id='client_3', original_billing_amount=150),
        InvoiceItem(invoice_date='2023-09-15', contract_id='client_1', original_billing_amount=200),
        InvoiceItem(invoice_date='2023-10-01', contract_id='client_2', original_billing_amount=275),
    ]

    queue_in = Queue()
    queue_out = Queue()
    consumer_thread = threading.Thread(target=consumer, args=(queue_in, queue_out))
    consumer_thread.start()

    for item in data:
        queue_in.put(item)
    queue_in.put(None)

    consumer_thread.join()
    results = [queue_out.get_nowait() for _ in range(queue_out.qsize())]

    # Verify the aggregation result
    it = iter(results)
    assert next(it, None) == ((2023, 9), 'client_1', 300.0)
    assert next(it, None) == ((2023, 9), 'client_2', 250.0)
    assert next(it, None) == ((2023, 9), 'client_3', 150.0)
    assert next(it, None) == ((2023, 10), 'client_2', 275.0)
    assert next(it, None) is None
