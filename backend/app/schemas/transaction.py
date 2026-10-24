from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class TransactionResponse(BaseModel):
    transaction_id: str
    account_number: str
    type: str
    channel: str
    category: str
    merchant: str
    amount: float
    status: str
    reference_number: Optional[str] = None
    timestamp: Optional[str] = None
    description: Optional[str] = None

class ExpenseBreakdownItem(BaseModel):
    category: str
    amount: float
    percentage: float
    count: int

class ExpenseAnalyticsResponse(BaseModel):
    total_spent: float
    period: str
    breakdown: List[ExpenseBreakdownItem]
    top_merchants: List[Dict[str, Any]]
    insights: List[str]
