from typing import Dict, Any
from ...services.banking_service import banking_service
from ...config.database import db

def handle_get_balance(user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    bal = banking_service.get_customer_balance(cid)
    return {"success": True, "status_code": 200, "data": bal}

def handle_get_remaining_funds(user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    res = banking_service.get_remaining_funds_analysis(cid)
    return {"success": True, "status_code": 200, "data": res}

def handle_get_db_status(user: Dict[str, Any]) -> Dict[str, Any]:
    status_info = db.get_status_info()
    return {"success": True, "status_code": 200, "data": status_info}
