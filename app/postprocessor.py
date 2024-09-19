from collections import defaultdict
from datetime import datetime

from dateutil.relativedelta import relativedelta

from app.model import PostprocessorOut, PostprocessorIn, YearMonth


def previous_month(year_month: YearMonth) -> YearMonth:
    date_obj = datetime(year=year_month[0], month=year_month[1], day=1)
    prev_month = date_obj - relativedelta(months=1)
    return prev_month.year, prev_month.month


def postprocess(data: list[PostprocessorIn]) -> list[PostprocessorOut]:
    client_ids = set()
    year_months = set()
    amounts: dict[tuple[YearMonth, str], float] = defaultdict(float)

    for year_month, contract_id, amount in data:
        amounts[(year_month, contract_id)] = amount
        client_ids.add(contract_id)
        year_months.add(year_month)

    results = []

    # here we loop over all possible year_months, from min to max
    min_year_month = min(year_months)
    max_year_month = max(year_months)
    start_date = datetime(min_year_month[0], min_year_month[1], 1)
    end_date = datetime(max_year_month[0], max_year_month[1], 1)
    for contract_id in client_ids:
        current_date = start_date
        while current_date <= end_date:
            year_month = (current_date.year, current_date.month)
            current_date += relativedelta(months=1)
            amount = amounts[(year_month, contract_id)]
            churned_ = 0
            if amount <= 0:
                last_month_amount = amounts[(previous_month(year_month), contract_id)]
                if last_month_amount > 0:
                    churned_ = last_month_amount
            if amount == 0 and churned_ == 0:
                # ignore if both amount and churned_ are 0
                continue
            results.append((year_month, contract_id, amount, churned_))

    return results
