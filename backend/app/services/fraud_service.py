from typing import Dict, Any, Optional
from ..banking_systems.fraud_system import fraud_system

class FraudService:
    @staticmethod
    def inspect_transaction(transaction_id: str, customer_id: Optional[str] = None) -> Dict[str, Any]:
        return fraud_system.verify_transaction(transaction_id, customer_id)

    @staticmethod
    def submit_dispute(customer_id: str, transaction_id: str, reason: str = "Unrecognized transaction") -> Dict[str, Any]:
        return fraud_system.create_dispute(customer_id, transaction_id, reason)

fraud_service = FraudService()
