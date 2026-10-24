from typing import Optional
from pydantic import BaseModel

class Dispute(BaseModel):
    dispute_id: str
    customer_id: str
    transaction_id: str
    reason: str
    amount: float
    status: str = "PENDING_REVIEW"  # PENDING_REVIEW, APPROVED, REJECTED, RESOLVED
    created_at: Optional[str] = None
    admin_notes: Optional[str] = None
    provisional_credit: bool = True
