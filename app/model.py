from app.api_model import InvoiceItem

ConsumerIn = InvoiceItem
YearMonth = tuple[int, int]
ConsumerOut = tuple[YearMonth, bytes, float]
PostprocessorIn = ConsumerOut
PostprocessorOut = tuple[YearMonth, bytes, float, float]
ProcessorOut = tuple[YearMonth, str, float, float]
