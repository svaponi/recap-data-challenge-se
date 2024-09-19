import uuid
from datetime import date
from typing import List

import pydantic


class InvoiceItem(pydantic.BaseModel):
    original_billing_amount: float
    contract_id: str
    invoice_id: str = pydantic.Field(default_factory=lambda: uuid.uuid4().hex)
    invoice_date: date


class ResponseBody(pydantic.BaseModel):
    data: List[InvoiceItem]
    total_pages: int
    page: int


class ApiResponse(pydantic.BaseModel):
    status_code: int
    body: ResponseBody
