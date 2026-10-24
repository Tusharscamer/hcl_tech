from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    customer_id: str
    name: str
    email: str
    phone: Optional[str] = None
    role: str = "customer"  # customer or admin
    kyc_status: str = "VERIFIED"
    monthly_income: float = 0.0
    risk_profile: str = "MODERATE"
    credit_score: int = 750
    created_at: Optional[str] = None
