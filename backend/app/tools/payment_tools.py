from typing import Dict, Any, Optional
from ..banking_systems.payment_system import payment_system

def get_payment_status(customer_id: str, query: Optional[str] = None, reference_number: Optional[str] = None) -> Dict[str, Any]:
    """
    Deterministic Tool: Verifies UPI transaction status, reference number, merchant and failure reason if any.
    """
    matches = payment_system.get_payment_status(customer_id, query=query, reference_number=reference_number)
    if not matches:
        return {
            "found": False,
            "customer_id": customer_id,
            "query": query or reference_number,
            "message": f"No payment transaction matching '{query or reference_number}' was found."
        }
    
    top = matches[0]
    return {
        "found": True,
        "customer_id": customer_id,
        "transaction_id": top.get("transaction_id"),
        "reference_number": top.get("reference_number"),
        "merchant": top.get("merchant"),
        "amount": top.get("amount"),
        "status": top.get("status"),
        "channel": top.get("channel"),
        "timestamp": top.get("timestamp"),
        "description": top.get("description"),
        "all_matches": matches
    }

def get_upcoming_payments(customer_id: str) -> Dict[str, Any]:
    """
    Deterministic Tool: Identifies upcoming card dues, EMIs, utility bills and subscriptions due this week/month.
    """
    bills = payment_system.get_upcoming_bills(customer_id)
    total_due = sum(b.get("amount", 0.0) for b in bills)

    return {
        "customer_id": customer_id,
        "count": len(bills),
        "total_amount_due": round(total_due, 2),
        "upcoming_bills": bills
    }
