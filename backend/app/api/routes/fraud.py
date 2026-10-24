from typing import Dict, Any
from ...services.fraud_service import fraud_service

def handle_fraud_verify(data: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    txn_id = data.get("transaction_id", "")
    res = fraud_service.inspect_transaction(txn_id, customer_id=cid)
    return {"success": True, "status_code": 200, "data": res}

def handle_submit_dispute(data: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
    cid = user.get("sub") or user.get("customer_id")
    txn_id = data.get("transaction_id", "")
    reason = data.get("reason", "Customer flagged unrecognized charge")
    res = fraud_service.submit_dispute(customer_id=cid, transaction_id=txn_id, reason=reason)
    return {"success": True, "status_code": 200, "data": res}
