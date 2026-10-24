from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class BalanceResponse(BaseModel):
    account_number: str
    available_balance: float
    ledger_balance: float
    currency: str = "INR"
    account_type: str = "SAVINGS"
    status: str = "ACTIVE"

class RemainingFundsResponse(BaseModel):
    available_balance: float
    total_upcoming_obligations: float
    estimated_remaining_funds: float
    obligations_breakdown: List[Dict[str, Any]]
    explanation: str

class CardDetailsResponse(BaseModel):
    card_id: str
    card_number: str
    card_type: str
    network: str
    card_holder: str
    status: str
    credit_limit: Optional[float] = None
    available_limit: Optional[float] = None
    statement_due_date: Optional[str] = None
    minimum_due: Optional[float] = None
    total_due: Optional[float] = None

class LoanDetailsResponse(BaseModel):
    loan_id: str
    loan_type: str
    sanctioned_amount: float
    outstanding_balance: float
    interest_rate: float
    emi_amount: float
    next_emi_date: str
    remaining_tenure_months: int
