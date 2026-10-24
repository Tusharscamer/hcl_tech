from typing import Optional
from pydantic import BaseModel

class Bill(BaseModel):
    bill_id: str
    customer_id: str
    biller_name: str
    category: str  # UTILITIES, TELECOM, SUBSCRIPTION, CREDIT_CARD, LOAN_EMI
    amount: float
    due_date: str
    status: str = "UPCOMING"  # UPCOMING, PAID, OVERDUE
    auto_pay: bool = False
