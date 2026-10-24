from typing import Dict, Any, Optional
from ..banking_systems.fraud_system import fraud_system

def fraud_verification(transaction_id: str, customer_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Deterministic Tool: Performs automated fraud check and risk scoring on transaction.
    """
    return fraud_system.verify_transaction(transaction_id=transaction_id, customer_id=customer_id)

def raise_dispute(customer_id: str, transaction_id: str, reason: str = "Unrecognized transaction") -> Dict[str, Any]:
    """
    Deterministic Tool: Opens a dispute workflow and routes to Human-in-the-Loop review.
    """
    return fraud_system.create_dispute(customer_id=customer_id, transaction_id=transaction_id, reason=reason)
