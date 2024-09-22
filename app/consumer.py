from collections import defaultdict
from queue import Queue

from app.model import YearMonth, ConsumerOut, ConsumerIn


def consumer(queue_in: Queue, queue_out: Queue):
    aggregated_data: dict[tuple[YearMonth, bytes], float] = defaultdict(float)

    while True:
        item: ConsumerIn = queue_in.get()
        if item is None:
            break

        try:
            contract_id = bytes.fromhex(item.contract_id)
        except:
            contract_id = str(item.contract_id).encode()

        amount = item.original_billing_amount
        year = item.invoice_date.year
        month = item.invoice_date.month
        aggregated_data[((year, month), contract_id)] += amount

    for (year_month, contract_id), total_amount in aggregated_data.items():
        _out: ConsumerOut = (
            year_month,
            contract_id,
            total_amount,
        )
        queue_out.put(_out)
