from app.api_model import InvoiceItem

ConsumerIn = InvoiceItem
YearMonth = tuple[int, int]
ConsumerOut = tuple[YearMonth, str, float]
PostprocessorIn = ConsumerOut
PostprocessorOut = tuple[YearMonth, str, float, float]
ProcessorOut = tuple[YearMonth, str, float, float]
