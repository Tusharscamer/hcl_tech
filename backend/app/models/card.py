from typing import Optional
from pydantic import BaseModel

class Card(BaseModel):
    card_id: str
    customer_id: str
    card_number: str
    card_type: str  # DEBIT, CREDIT
    network: str = "VISA"  # VISA, MASTERCARD, RUPAY
    card_holder: str
    expiry_date: str
    status: str = "ACTIVE"  # ACTIVE, BLOCKED, EXPIRED
    daily_limit: Optional[float] = 50000.0
    credit_limit: Optional[float] = None
    available_limit: Optional[float] = None
    statement_due_date: Optional[str] = None
    minimum_due: Optional[float] = None
    total_due: Optional[float] = None
    international_enabled: bool = False
    contactless_enabled: bool = True
