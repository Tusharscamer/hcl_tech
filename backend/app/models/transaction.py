from typing import Optional
from pydantic import BaseModel

class Transaction(BaseModel):
    transaction_id: str
    account_number: str
    customer_id: str
    type: str  # DEBIT, CREDIT
    channel: str  # UPI, POS, CARD, NETBANKING, NEFT
    category: str  # Food, Transport, Shopping, Bills, etc.
    merchant: str
    amount: float
    status: str = "COMPLETED"  # COMPLETED, PENDING, FAILED, FLAGGED
    reference_number: Optional[str] = None
    timestamp: Optional[str] = None
    description: Optional[str] = None
