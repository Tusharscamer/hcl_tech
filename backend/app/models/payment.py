from typing import Optional
from pydantic import BaseModel

class Payment(BaseModel):
    payment_id: str
    customer_id: str
    recipient: str
    amount: float
    channel: str = "UPI"  # UPI, IMPS, NEFT, RTGS
    status: str = "COMPLETED"  # COMPLETED, PENDING, FAILED
    reference_number: str
    timestamp: Optional[str] = None
    remarks: Optional[str] = None
