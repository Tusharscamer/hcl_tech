from typing import Dict, Any
from ...services.payment_service import payment_service

def handle_get_bills(user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    bills = payment_service.get_upcoming_bills(cid)
    return {"success": True, "status_code": 200, "data": bills}

def handle_payment_status(user: Dict[str, Any], query_params: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    query = query_params.get("query")
    ref = query_params.get("reference")
    res = payment_service.check_payment_status(cid, query=query, ref=ref)
    return {"success": True, "status_code": 200, "data": res}
