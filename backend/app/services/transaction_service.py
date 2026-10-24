from typing import Dict, Any, List, Optional
from ..config.database import db
from ..calculations.expenses import aggregate_expenses_by_category

class TransactionService:
    @staticmethod
    def get_recent_transactions(customer_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        txns = db.find("transactions", {"customer_id": customer_id})
        txns = sorted(txns, key=lambda x: x.get("timestamp", ""), reverse=True)
        return txns[:limit]

    @staticmethod
    def get_spending_analytics(customer_id: str) -> Dict[str, Any]:
        txns = db.find("transactions", {"customer_id": customer_id})
        return aggregate_expenses_by_category(txns)

transaction_service = TransactionService()
