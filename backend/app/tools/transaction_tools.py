from typing import Dict, Any, List, Optional
from ..config.database import db

def get_transactions(customer_id: str, limit: int = 10, category: Optional[str] = None) -> Dict[str, Any]:
    """
    Deterministic Tool: Retrieves recent transactions, credits and debits.
    """
    txns = db.find("transactions", {"customer_id": customer_id})
    if category:
        txns = [t for t in txns if t.get("category", "").lower() == category.lower()]
    
    # Sort descending by timestamp
    txns = sorted(txns, key=lambda x: x.get("timestamp", ""), reverse=True)
    
    recent = txns[:limit]
    total_debits = sum(t["amount"] for t in txns if t["type"] == "DEBIT")
    total_credits = sum(t["amount"] for t in txns if t["type"] == "CREDIT")

    return {
        "customer_id": customer_id,
        "count": len(recent),
        "total_records": len(txns),
        "total_debits": total_debits,
        "total_credits": total_credits,
        "transactions": recent
    }
