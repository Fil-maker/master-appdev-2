from pydantic import BaseModel


class ReportResponse(BaseModel):
    report_at: str
    order_id: int
    stock_quantity: int
