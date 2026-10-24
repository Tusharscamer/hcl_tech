from typing import Dict, Any
from ...services.loan_service import loan_service

def handle_get_loans(user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    loans = loan_service.get_loans(cid)
    return {"success": True, "status_code": 200, "data": loans}

def handle_get_loan_eligibility(user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    elig = loan_service.get_eligibility(cid)
    return {"success": True, "status_code": 200, "data": elig}
