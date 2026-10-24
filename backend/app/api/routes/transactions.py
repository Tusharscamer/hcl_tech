from typing import Dict, Any
from ...services.transaction_service import transaction_service

def handle_get_transactions(user: Dict[str, Any], query_params: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    limit = int(query_params.get("limit", 20))
    txns = transaction_service.get_recent_transactions(cid, limit=limit)
    return {"success": True, "status_code": 200, "data": txns}

def handle_get_expense_analytics(user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    analytics = transaction_service.get_spending_analytics(cid)
    return {"success": True, "status_code": 200, "data": analytics}
