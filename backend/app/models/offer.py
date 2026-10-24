from typing import Optional
from pydantic import BaseModel

class Offer(BaseModel):
    offer_id: str
    customer_id: str
    offer_type: str  # PRE_APPROVED_LOAN, CREDIT_LIMIT_INCREASE, FIXED_DEPOSIT
    title: str
    description: str
    max_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    max_tenure_months: Optional[int] = None
    new_limit: Optional[float] = None
    valid_until: Optional[str] = None
    status: str = "AVAILABLE"  # AVAILABLE, ACCEPTED, EXPIRED
