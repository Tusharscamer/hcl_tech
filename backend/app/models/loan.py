from typing import Optional
from pydantic import BaseModel

class Loan(BaseModel):
    loan_id: str
    customer_id: str
    loan_type: str  # HOME_LOAN, PERSONAL_LOAN, AUTO_LOAN
    sanctioned_amount: float
    outstanding_balance: float
    interest_rate: float
    tenure_months: int
    remaining_tenure_months: int
    emi_amount: float
    next_emi_date: str
    status: str = "ACTIVE"
    auto_debit_account: Optional[str] = None
    purpose: Optional[str] = None
