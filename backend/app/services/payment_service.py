from typing import Dict, Any, List, Optional
from ..banking_systems.payment_system import payment_system

class PaymentService:
    @staticmethod
    def get_upcoming_bills(customer_id: str) -> List[Dict[str, Any]]:
        return payment_system.get_upcoming_bills(customer_id)

    @staticmethod
    def check_payment_status(customer_id: str, query: Optional[str] = None, ref: Optional[str] = None) -> List[Dict[str, Any]]:
        return payment_system.get_payment_status(customer_id, query=query, reference_number=ref)

payment_service = PaymentService()
