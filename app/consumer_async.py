import asyncio
from collections import defaultdict
from typing import Tuple

from app.model import YearMonth, ConsumerIn, ConsumerOut


async def consumer(queue_in: asyncio.Queue, queue_out: asyncio.Queue):
    aggregated_data: dict[Tuple[YearMonth, str], float] = defaultdict(float)

    while True:
        item: ConsumerIn = await queue_in.get()
        if item is None:
            break

        contract_id = item.contract_id
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
        await queue_out.put(_out)
