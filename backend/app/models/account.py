from typing import Optional
from pydantic import BaseModel

class Account(BaseModel):
    account_number: str
    customer_id: str
    account_type: str = "SAVINGS"  # SAVINGS, CURRENT
    currency: str = "INR"
    available_balance: float
    ledger_balance: float
    status: str = "ACTIVE"
    branch: Optional[str] = "Main Branch"
    ifsc_code: Optional[str] = "APEX0001042"
    is_primary: bool = True
    opened_date: Optional[str] = None
